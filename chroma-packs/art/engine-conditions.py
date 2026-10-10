# Chroma content pack: Art and Writing. Proposed engine conditions, in the shape of ../stage/engine-conditions.py and
# earth_rules.PACK_RULES (ECHO: anchor at the time of the anchor moment; req, more, less when the echo comes; READ: who
# an outside event can come to; LIFE: who a life event can come to, read by batch.py as the moment's gate). Plain data
# for the Engine, which owns PACK_RULES (it pastes these with calib_v7/paste_pack_rules.py) and may reword anything.
# JUST is earth_rules.JUST. Every anchor names a base moment (the pack never edits base moments), one of this pack's
# own moments, or a condition the engine already reads. Pathways and packs thread, 2026-10-10 (v22.4, held).
JUST = 1 / 12
ECHO_ART = {
    # the urge to make something, or an idea, in someone who drew at school: the old sketchbook comes out of the attic
    # (the door from childhood back to the taste rung)
    "the sketchbook in the attic": dict(
        anchor=f"had(['the urge to make something', 'inspiration strikes'], {JUST}) & has('drawing and painting') & "
               "(age >= 30)",
        req="~has('life-drawing regular') & ~has('painter or sculptor') & ~has('street artist') & "
            "~has('illustrator for hire')",
        more=["(hR + hU) > .5", "time > .5", "retired"],
        less=["stress > 1.5", "kids_home > 1", "money < .1"]),
    # after a loss or in the first months of retirement, someone who wrote finds the notebook again (the late poet's door)
    "the poems you never showed anyone": dict(
        anchor=f"had(['the first months of retirement', 'your partner dies', 'the notebooks come together'], {JUST}) & "
               "(has('writing poems') | has('writing stories'))",
        req="(age >= 25) & ~has('open-mic poet') & ~has('novelist')",
        more=["(hR + hW) > .5", "time > .4"],
        less=["stress > 1.8", "health < .3"]),
}
READ_ART = {
    # the reviews after a show: only to someone whose work was on show
    "the reviews of the show are in": dict(
        req="has('painter or sculptor') | has('renowned artist') | has('street artist') | has('illustrator for hire') | "
            "has('master craftsperson')",
        more=["has('renowned artist')", "has('a name in the art world')"],
        less=["~has('a name in the art world') & ~has('a dealer who sells your work')"]),
}

# The rung below (Emren 10-06 09:18; engine 10:38): a life event that gives a career or a summit comes only to someone
# on the rung below it with a year or more on it (two or more for a summit), or one rung below that after years on it;
# never to a perk alone. The moment's holds: names the rungs; these gates add the exact years where one tenure: cannot
# say them.
LIFE_ART = {
    "art school applications": dict(req="~was('art school student') & (age <= 35)"),
    "a wall that needs a mural": dict(req="(yrs_has('life-drawing regular') >= 1) | has('art school student') | "
                                          "has('art teacher')"),
    "the first commission": dict(req="~has('illustrator for hire') & ((yrs_has('life-drawing regular') >= 2) | "
                                     "has('art school student') | (yrs_has('street artist') >= 1))"),
    "the first show": dict(req="~has('painter or sculptor') & ((yrs_has('life-drawing regular') >= 4) | "
                               "(yrs_has('street artist') >= 2) | (yrs_has('illustrator for hire') >= 3) | "
                               "(yrs_has('art school student') >= 2))"),
    "the school needs an art teacher": dict(req="~has('art teacher') & (has('teacher') | was('art school student') | "
                                                "(yrs_has('painter or sculptor') >= 2) | "
                                                "(yrs_has('illustrator for hire') >= 2) | "
                                                "(yrs_has('street artist') >= 2))"),
    "an empty shop on the corner": dict(req="~has('gallery owner') & ((yrs_has('painter or sculptor') >= 3) | "
                                            "(yrs_has('art teacher') >= 5) | (yrs_has('shop owner') >= 3) | "
                                            "(yrs_has('museum curator') >= 3) | (yrs_has('illustrator for hire') >= 5))"),
    "the guild judges your masterpiece": dict(req="~has('master craftsperson') & ((yrs_has('craft maker') >= 4) | "
                                                  "(yrs_has('carpenter') >= 6))"),
    "a publisher reads the manuscript": dict(req="has('novelist') | (yrs_has('open-mic poet') >= 2) | "
                                                 "(yrs_has('illustrator for hire') >= 2)"),
    "a work in the national collection": dict(req="~has('renowned artist') & ((yrs_has('painter or sculptor') >= 5) | "
                                                  "(yrs_has('street artist') >= 5) | "
                                                  "(yrs_has('illustrator for hire') >= 5) | "
                                                  "(yrs_has('master craftsperson') >= 5))"),
    "a national prize for writing": dict(req="~has('celebrated author') & (yrs_has('novelist') >= 3)"),
    # the world-only steps (art-worlds.lib)
    "the painted cave at the winter camp": dict(req="(yrs_has('painter or sculptor') >= 2) | "
                                                    "(yrs_has('street artist') >= 2) | "
                                                    "(yrs_has('life-drawing regular') >= 3) | has('art school student')"),
    "the carver's mask for the dead": dict(req="(yrs_has('craft maker') >= 4) | has('master craftsperson') | "
                                               "has('painter or sculptor')"),
    "the queen's portrait sitting": dict(req="(yrs_has('painter or sculptor') >= 3) | "
                                             "(yrs_has('illustrator for hire') >= 3)"),
    "the illuminated book for the cathedral": dict(req="has('illustrator for hire') | has('art school student') | "
                                                       "(yrs_has('life-drawing regular') >= 2)"),
}

# ---------------------------------------------------------------- long shots (art-longshots.lib)
# A long shot is a bold try at the next rung, or a skip of at most one rung by someone with years on the rung below
# (Emren 10-06 09:18). Every one-colour option at chance 1 to 5 that gives a title carries `grants_if_fails: a long
# shot that missed` (core/longshot.py). The echoes anchor on that perk, one of these moments within JUST, and the
# engine's clock ago_fail_long within JUST (set only by a real long-shot miss), so they speak of this attempt and not of
# a perk held from another pack. The second try offers `title: {missed}`.
LONGSHOTS_ART = ['the sketch that went round the world', 'the open submission to the great summer show',
                 'the manuscript in the pile on the floor', 'the late starter at the easel',
                 'the other side of the easel', 'the judge stops at your table at the craft fair']
LIFE_ART_LONGSHOTS = {
    "the sketch that went round the world": dict(
        req="~has('painter or sculptor') & ((yrs_has('life-drawing regular') >= 2) | (yrs_has('street artist') >= 2) | "
            "(yrs_has('illustrator for hire') >= 2))"),
    "the open submission to the great summer show": dict(
        req="~has('renowned artist') & ((yrs_has('painter or sculptor') >= 2) | (yrs_has('life-drawing regular') >= 5))"),
    "the manuscript in the pile on the floor": dict(
        req="~has('celebrated author') & ((yrs_has('open-mic poet') >= 2) | (yrs_has('novelist') >= 3))"),
    "the late starter at the easel": dict(
        req="~was('painter or sculptor') & (yrs_has('life-drawing regular') >= 2)"),
    "the other side of the easel": dict(
        req="~has('gallery owner') & ((yrs_has('painter or sculptor') >= 3) | (yrs_has('illustrator for hire') >= 3) | "
            "(yrs_has('art teacher') >= 3))"),
    "the judge stops at your table at the craft fair": dict(
        req="~has('renowned artist') & ((yrs_has('craft maker') >= 3) | (yrs_has('master craftsperson') >= 5))"),
}
ECHO_ART_LONGSHOTS = {
    # the second try: years later the same kind of door opens a crack, and the try is for the same title again
    "the same canvas, years later": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_ART!r}, {JUST}) & (ago_fail_long < {JUST})",
        req="(age >= 18) & ~has('renowned artist') & ~has('celebrated author')",
        more=["has('drawing and painting') | has('writing poems') | has('writing stories')", "(hR + hB) > .5",
              "time > .4"],
        less=["stress > 1.5", "money < .15", "health < .4"]),
    # making peace with it: the long shot becomes a class taught, a circle kept, a rung open to anyone
    "the long shot becomes a class to teach": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_ART!r}, {JUST}) & (ago_fail_long < {JUST})",
        req="(age >= 25) & ~has('renowned artist') & ~has('celebrated author')",
        more=["sa > 10", "has('teaching') | has('art teacher') | has('pupils who remember you')", "(hW + hG) > .5"],
        less=["stress > 1.5", "health < .3"]),
}
