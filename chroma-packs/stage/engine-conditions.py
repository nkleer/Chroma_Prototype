# Chroma content pack: Stage and Screen. Proposed engine conditions for the pack's four echoes and its read event, in
# the shape of earth_rules.PACK_RULES["science"] (ECHO: anchor at the time of the anchor moment; req, more, less when
# the echo comes; READ: who an outside event can come to). Plain data for the engine thread, which owns PACK_RULES and
# may reword anything. JUST is earth_rules.JUST. The pack has no inner moments outside its threshold seasons, and a
# season's moments (threshold:) need none. Every anchor names a base moment (the pack never edits base moments) or a
# condition the engine already reads.
JUST = 1 / 12
ECHO_STAGE = {
    # the school play as a child, back years later when a notice for the local players or an open audition turns up
    # (the door from childhood: youth theatre, the local players, drama school, the extra's day)
    "the part you never got to play": dict(
        anchor=f"had(['the school play'], {JUST}) & (age < 13)",
        req="(age >= 18) & ~has('amateur actor') & ~has('professional actor')",
        more=["(hR + hG) > .5", "time > .5", "has('singing') | has('dancing')"],
        less=["stress > 1.5", "money < .15", "held_children & (kids_home > 0) & (time < .3)"]),
    # the first months of retirement, and a notice for the local players or the film in town (the late bloomer's door:
    # the lead at seventy)
    "never too late for the stage": dict(
        anchor=f"had(['the first months of retirement'], {JUST})",
        req="retired & ~has('amateur actor') & (health > .4)",
        more=["was('amateur actor') | was('youth theatre member') | has('a lead role to remember')", "time > .5",
              "(hG + hR) > .45"],
        less=["health < .5", "money < .15", "held_partner & (support < .3)"]),
    # an idea that will not let go, or the wish to be seen, in someone who can act: the one-person show and the fringe
    # (the raw talent's door)
    "the show you wrote to star in": dict(
        anchor=f"had(['inspiration strikes', 'wanting to be noticed'], {JUST}) & has('acting')",
        req="(age >= 17) & ~has('lead actor or actress') & ~has('a fringe slot')",
        more=["has('writing stories') | has('writing scripts')", "has('improvisation')", "(hR + hU) > .5"],
        less=["stress > 1.5", "money < .15", "kids_home > 1"]),
    # the base chance of a role turns into a part for someone who can act and is on the rung below a paid part (the
    # door from a lucky letter): two years with the local players or as an extra, or a year at drama school
    "the part that came with the letter": dict(
        anchor=f"had(['an unexpected chance: a grant, a role, a stage'], {JUST}) & has('acting')",
        req="(age >= 17) & ~has('professional actor') & ((yrs_has('amateur actor') >= 2) | "
            "(yrs_has('background artist') >= 2) | (yrs_has('drama school student') >= 1))",
        more=["has('a lead role to remember')", "has('amateur actor')", "has('casting directory listing')"],
        less=["stress > 1.5", "kids_home > 1", "health < .4"]),
}
# The rung below (Emren 09:18; engine 10:38): a life event that gives a career or a summit comes only to someone on
# the rung below it with a year or more on it (two for a summit), or one rung below that after years on it; never to a
# perk alone (acting, a lead role to remember, writing stories, a fringe slot). The moment's holds: names the rungs and
# req adds the years (earth_rules.LIFE's shape, for PACK_RULES["stage"]["LIFE"]); a moment whose rungs all need the
# same years carries `tenure:` in its .lib instead.
_LEAD_RUNG = ("(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) | "
              "((yrs_has('amateur actor') >= 5) & has('a lead role to remember'))")
LIFE_STAGE = {
    # the lead, from a working actor of two years; an amateur of five years with a lead behind them is the one rung
    # skipped (the non-professional cast in a lead: real, but rare)
    "the part of a lifetime is cast": dict(req=_LEAD_RUNG),
    "chosen to wear the great mask": dict(req=_LEAD_RUNG),
    "a glamour that makes the play real": dict(req=_LEAD_RUNG),
    # the understudy goes on after a year or more as a professional actor
    "the understudy goes on": dict(req="has('understudy') & (yrs_has('professional actor') >= 1)"),
    # the director's next lead goes to a working actor of two years, not to a bond that outlives the career
    "the director calls again": dict(req="has('a director who keeps casting you') & "
                                         "((yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2))"),
    # the fringe's paid parts ([professional actor]) go to someone in work, or with a year or more on the rung below
    "opening night at the fringe": dict(req="has('a fringe slot') & (has('professional actor') | has('voice actor') | "
                                            "(yrs_has('drama school student') >= 1) | "
                                            "(yrs_has('amateur actor') >= 2) | (yrs_has('background artist') >= 2))"),
    # voice work: a professional actor of a year, or an amateur or a radio voice of two years with accents and voices
    "a voice for the cartoon": dict(req="(yrs_has('professional actor') >= 1) | (has('accents and voices') & "
                                        "((yrs_has('amateur actor') >= 2) | "
                                        "(yrs_has('community-radio presenter') >= 2)))"),
    # stage management: a year at the technician's bench or at drama school, or two years with the local players
    "the stage management team is a person short": dict(
        req="(yrs_has('stage technician') >= 1) | (yrs_has('drama school student') >= 1) | "
            "(yrs_has('amateur actor') >= 2) | (yrs_has('community theatre director') >= 2)"),
    # the autumn play: a player or a drama teacher of three years is asked to run the society; its director (who alone
    # can take the professional company's offer, [director]) is asked again only after three years running it
    "a director is needed for the autumn play": dict(
        req="(~has('community theatre director') & ((yrs_has('amateur actor') >= 3) | "
            "(yrs_has('drama teacher') >= 3))) | (yrs_has('community theatre director') >= 3)"),
    # the playwright: a novelist or a journalist of a year, or two years of writing with a stage history
    "the script competition": dict(
        req="(yrs_has('novelist') >= 1) | (yrs_has('journalist') >= 1) | (((yrs_has('writing stories') >= 2) | "
            "(yrs_has('writing scripts') >= 2)) & (was('amateur actor') | was('community theatre director') | "
            "was('drama school student') | was('professional actor')))"),
    # the illusionists' wagons are open to anyone for the triads; a player's place (the singles, for [amateur actor]
    # only) needs a year with the town's players, so an amateur of less than a year waits for the next company
    "the illusionist players come to town": dict(req="~has('amateur actor') | (yrs_has('amateur actor') >= 1)"),
    # Round 5, 2026-10-07 (checklist P16): the town's director or a company of one's own, three years on (holds: and
    # tenure: in the .lib), asked to take the show to the city's theatre: no gate beyond the lib's
    # the school's drama post, for a teacher of two years (holds: and tenure:) who can act or has run or played with the
    # local players: the rung below [drama teacher] (roles.py rungs=)
    "the school needs someone to take drama": dict(
        req="has('acting') | was('amateur actor') | was('community theatre director')"),
}
READ_STAGE = {
    # the notices after an opening: only to someone whose work was on show (the moment's holds: says the same)
    "the reviews are in": dict(
        req="has('professional actor') | has('lead actor or actress') | has('director') | "
            "has('playwright or screenwriter') | has('amateur actor') | has('community theatre director')",
        more=["has('lead actor or actress')", "has('a fringe slot')"],
        less=["~has('lead actor or actress') & has('amateur actor')"]),
}


# ---------------------------------------------------------------- long shots (merged 2026-10-06 with stage-longshots.lib)
# Chroma content pack: Stage and Screen, LONG SHOTS (draft 2, 2026-10-06). Proposed engine conditions for
# stage-longshots.lib, in the shape of stage/engine-conditions.py and earth_rules.PACK_RULES: ECHO (anchor at the time
# of the anchor moment; req, more, less when the echo comes) and LIFE (who a life event can come to; batch.py reads
# PACK_RULES[pack]["LIFE"] as the moment's gate). Plain data for the engine thread, which owns PACK_RULES and may
# reword anything. JUST is earth_rules.JUST.
#
# LIFE gates (draft 2, after Emren's 09:18): a long shot is a bold try at the next rung, or a skip of at most one rung
# by someone with years on the rung below. The lib's `holds:` and `tenure:` already keep each moment to the rung below;
# these gates make the years exact (yrs_has) where one tenure cannot say it, using the ladders the shared files use
# (coordinator, 2026-10-06). The echoes cannot load without this file, so the gates travel with them.
#
# ECHO anchors: the perk 'a long shot that missed' (core/longshot.py), one of this file's own long-shot moments within
# JUST, and the engine's clock ago_fail_long within JUST (engine 08:21: set only by a real long-shot miss, true odds
# under .1), so the echo speaks of this attempt and not of a perk held from Politics or Science. The second try offers
# `title: {missed}`, the title that missed.
# Round 5, 2026-10-07 (checklist P9): LONGSHOTS_STAGE now names every Stage moment with a one-color long shot (chance 1
# to 5 that gives a title), all of which carry `grants_if_fails: a long shot that missed`: the seven long-shot moments of
# stage-longshots.lib (LS7 'the other side of the table' is new) and the five step moments whose singles are long
# shots ('an open audition in the city', 'a voice for the cartoon', 'the stage management team is a person short',
# 'the old teller dies at midwinter', 'the illusionist players come to town'). LONGSHOTS_STAGE_PROPOSED is retired:
# 'the part of a lifetime is cast', 'a screen test', 'the script competition', 'opening night at the fringe' and 'the
# part that came with the letter' stay steps at real odds (6 to 58), not long shots, so they carry no perk.
JUST = 1 / 12
LONGSHOTS_STAGE = ['the lead from the open queue', 'filmed by chance in the street', 'the film you made with friends',
                   'the old theatre needs someone to save it', 'the late starter', 'the night both covers are off',
                   'the other side of the table',
                   'an open audition in the city', 'a voice for the cartoon',
                   'the stage management team is a person short', 'the old teller dies at midwinter',
                   'the illusionist players come to town']
LIFE_STAGE_LONGSHOTS = {
    # the lead from the rung below (professional or voice actor, understudy), or the one-rung skip: an amateur with
    # five years on the local stage and a lead role to remember (holds: names the four titles)
    "the lead from the open queue": dict(
        req="~has('lead actor or actress') & (has('professional actor') | has('voice actor') | has('understudy') | "
            "((yrs_has('amateur actor') >= 5) & has('a lead role to remember')))"),
    # a performer with three years or more in public (holds: and tenure: 3-99); not yet paid for it
    # Round 5, 2026-10-07 (checklist P8, from nothing): the three years must be on a rung below [professional actor],
    # with the local players or as an extra; a busker or a local name alone no longer meets the moment
    "filmed by chance in the street": dict(
        req="~has('professional actor') & ~has('voice actor') & "
            "((yrs_has('amateur actor') >= 3) | (yrs_has('background artist') >= 3))"),
    # writing for years (holds: and tenure: 4-99) plus a stage or screen history, for [playwright or screenwriter]
    # Round 5, 2026-10-07 (checklist P8, from nothing): the stage history must be a rung in [playwright or
    # screenwriter]'s rungs= (roles.py); a youth theatre past or a perk alone (acting, stagecraft, a fringe slot,
    # editing) no longer counts
    "the film you made with friends": dict(
        req="~has('playwright or screenwriter') & (has('novelist') | has('journalist') | was('amateur actor') | "
            "was('community theatre director') | was('professional actor') | was('drama school student'))"),
    # a director with three years, or a community theatre director with many (eight) years, for [artistic director]
    "the old theatre needs someone to save it": dict(
        req="~has('artistic director') & ((yrs_has('director') >= 3) | (yrs_has('community theatre director') >= 8))"),
    # two years or more as an amateur or an extra (holds: and tenure: 2-99), never paid for acting before
    "the late starter": dict(
        req="~was('professional actor') & ~was('voice actor')"),
    # the company and its crew; the lead options themselves require [professional actor] (understudies hold it)
    "the night both covers are off": dict(
        req="~has('lead actor or actress')"),
    # Round 5, 2026-10-07 (checklist P9): a professional actor of three years (holds: and tenure: 3-99), not the lead
    "the other side of the table": dict(
        req="~has('lead actor or actress')"),
}
ECHO_STAGE_LONGSHOTS = {
    # the second try: years later the same kind of door opens a crack, and the try is for the same title again
    # (`title: {missed}`), a little likelier (4 against 2 or 3); not for someone who has since made the lead or runs a
    # theatre
    "the same door, years later": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_STAGE!r}, {JUST}) & (ago_fail_long < {JUST})",
        req="(age >= 21) & ~has('lead actor or actress') & ~has('artistic director')",
        more=["has('acting') | has('writing scripts') | has('directing actors') | has('amateur actor')",
              "(hR + hB) > .5", "time > .4"],
        less=["stress > 1.5", "money < .15", "health < .4"]),
    # making peace with it: the long shot becomes a story told to someone younger, a class, a fund, the local players
    # (an entry rung open to anyone, `title: amateur actor`)
    "the long shot becomes a story to tell": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_STAGE!r}, {JUST}) & (ago_fail_long < {JUST})",
        req="(age >= 25) & ~has('lead actor or actress')",
        more=["sa > 10", "has('teaching') | has('telling a story aloud') | has('acting')", "(hW + hG) > .5"],
        less=["stress > 1.5", "health < .3"]),
}
