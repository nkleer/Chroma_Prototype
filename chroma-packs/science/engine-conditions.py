# Chroma content pack: Science, long shots (LONGSHOTS-BRIEF.md, 2026-10-06; round 2 after the 09:21 brief). Proposed
# engine conditions for the pack's long-shot moments and for the two echoes anchored on the shared perk [a long shot
# that missed] (chroma-packs/core/longshot.py), in the shape of earth_rules.PACK_RULES["science"] (ECHO: anchor at the
# time of the attempt; req, more, less when the echo comes. LIFE: req, the gate on who meets a life event at all). Plain
# data for the engine thread, which owns PACK_RULES and may reword anything. Merged into the pack 2026-10-06 with
# science-longshots.lib. JUST is earth_rules.JUST. Only the long-shot moments are here; the pack's other echoes are in PACK_RULES.
#
# Round 2 (Emren 09:18: big titles take consecutive steps, commitment and tries). The LIFE gates below are what make
# each try a step: each long shot is met only by someone with years on the rung below (yrs_has) and the rest of that
# rung (a grant, a skill, a publication). The moments' holds: and tenure: in the .lib say the same in coarser form (the
# shortest years among the titles named), so a merge that drops these gates still keeps the newcomer out.
JUST = 1 / 12

# the long-shot life events of science-longshots.lib
LS_DISCOVERY = "a discovery nobody asked you for"
LS_GROUP = "a group of your own, open to all comers"
LS_FACILITY = "a facility looks outside for its next head"
LS_VOICE = "a search for a new voice for science"   # round 5: a long shot at 5 (it was an entry step at 10)
# Round 5, 2026-10-07 (checklist P9): a long shot for every career and summit of the pack, each from the rung below
LS_CHAIR = "a chair falls vacant at another university"        # professor
LS_FAMOUS_LAB = "a scientist's post at a famous lab"            # research scientist
LS_FELLOWSHIP = "a named fellowship, one a year"                # postdoctoral researcher
LS_CENTRE = "a national centre opens its posts"                 # the side roads and the project lead, one per color
LS_SURVEY = "the survey wants a paid assistant"                 # research assistant, from the amateur side
SECOND_TRY = "the old door opens a crack"
LONGSHOTS_SCIENCE = [LS_DISCOVERY, LS_GROUP, LS_FACILITY, LS_VOICE, LS_CHAIR, LS_FAMOUS_LAB, LS_FELLOWSHIP, LS_CENTRE,
                     LS_SURVEY]
# the tries for a title, whose title the second try offers again (`title: {missed}`); round 5: all of them
LONGSHOTS_TITLE = list(LONGSHOTS_SCIENCE)
_MISSED_HERE = f"(ago_fail_long <= {JUST})"   # the long shot failed in this moment (engine clock, 08:21)
_SINCE = 14   # years: the second try comes 3 to 12 years after the anchor (its delay:), so the attempt is within this

# Who is still on the rung below each summit, years later (the second try's req, one branch per attempt).
_STILL_ON_RUNG = {
    LS_DISCOVERY: "~has('independent investigator') & has('published research') & (has('research scientist') | "
                  "has('research assistant') | has('citizen scientist') | has('community observer') | "
                  "has('volunteer research organiser'))",
    LS_GROUP: "~has('research group leader') & has('research grant') & (has('research scientist') | "
              "has('research project lead'))",
    # Round 5 (P1): the hands-on skill, [lab work] or the troubleshooting that comes on top of it
    LS_FACILITY: "~has('research facility lead') & (has('lab work') | has('instrument troubleshooting')) & "
                 "(has('laboratory technician') | has('research scientist'))",
    # Round 5 (P9): the same for the tries added in round 5
    LS_VOICE: "~has('science communication specialist') & has('explaining science') & (has('research scientist') | "
              "has('research assistant') | has('journalist') | has('teacher'))",
    LS_CHAIR: "~has('professor') & has('published research') & (has('research group leader') | has('research scientist'))",
    LS_FAMOUS_LAB: "~has('research scientist') & (has('research assistant') | has('laboratory technician') | "
                   "has('research data steward') | has('research software engineer'))",
    LS_FELLOWSHIP: "~has('postdoctoral researcher') & has('doctoral graduate') & has('research scientist') & "
                   "(yrs_has('research scientist') <= 8)",
    LS_CENTRE: "has('research scientist')",   # still a scientist, not yet on the road the first try aimed at
    LS_SURVEY: "~has('research assistant') & (has('citizen scientist') | has('community observer'))",
}

ECHO_SCIENCE_LONGSHOTS = {
    # the second try (commitment): years after a missed try for a title, the same kind of door opens a crack; the
    # .lib offers the very title missed (`title: {missed}`) at 7 against the first try's 3 to 5, and only to someone
    # still on the rung below it (the branch for the attempt they made)
    SECOND_TRY: dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_TITLE!r}, {JUST}) & {_MISSED_HERE}",
        req="(age >= 28) & (age <= 85) & (health > .35) & ("
            + " | ".join(f"(had([{nm!r}], {_SINCE}) & {cond})" for nm, cond in _STILL_ON_RUNG.items()) + ")",
        more=["has('mentor') | has('research collaborators')",
              "has('research grant') | has('savings') | has('patron')",
              "has('a finding that held up') | has('name in the field') | has('supervising researchers')"],
        less=["stress > 1.5", "money < .15", "held_children & (kids_home > 0) & (time < .3)"]),
    # making peace with it: years after any of the tries (a second try that missed included), someone asks, and the
    # person finds out how the story is told now (teaching, the honest account, cheering someone younger, letting it
    # rest); the peace reading can name it
    "the story of the long shot": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_SCIENCE + [SECOND_TRY]!r}, {JUST}) & {_MISSED_HERE}",
        req="age >= 32",
        more=["retired", "kids_home == 0",
              "has('teaching') | has('explaining science') | has('former students') | has('mentor')"],
        less=["stress > 1.5", "health < .25", "ago_loss < 1"]),
}

# The LIFE gates (earth_rules.LIFE shape, merged by batch over R.LIFE): years on the rung below, and the rest of it.
LIFE_SCIENCE_LONGSHOTS = {
    # research practice of some years: a scientist 2+, an assistant 3+, or a long-time volunteer (citizen scientist or
    # community observer 5+, organiser 3+) who already has a publication; the singles also need [published research]
    LS_DISCOVERY: dict(req="~has('independent investigator') & ((yrs_has('research scientist') >= 2) | "
                           "(yrs_has('research assistant') >= 3) | (has('published research') & "
                           "((yrs_has('citizen scientist') >= 5) | (yrs_has('community observer') >= 5) | "
                           "(yrs_has('volunteer research organiser') >= 3))))"),
    # a research scientist (postdoc or not) of four years or more, with a grant in hand: a skip of the project-lead rung
    LS_GROUP: dict(req="~has('research group leader') & (yrs_has('research scientist') >= 4) & has('research grant')"),
    # Round 5, 2026-10-07 (P1): a technician or a scientist of four years or more with the hands-on skill ([lab work],
    # or the troubleshooting that comes on top of it): the next rung, outside (was six years and the troubleshooting)
    LS_FACILITY: dict(req="~has('research facility lead') & ((yrs_has('laboratory technician') >= 4) | "
                          "(yrs_has('research scientist') >= 4)) & (has('lab work') | has('instrument troubleshooting'))"),
    # Round 5, 2026-10-07 (P9, Emren 09:18): now a long shot; three years or more of explaining science and a degree,
    # with one of the communicator's rungs below in roles.py behind it (a research post, journalism or teaching)
    LS_VOICE: dict(req="~has('science communication specialist') & (yrs_has('explaining science') >= 3) & "
                       "has('graduate') & (was('research scientist') | was('research assistant') | was('journalist') | "
                       "was('teacher'))"),
    # Round 5, 2026-10-07 (P9): the tries added in round 5, each from the rung below its title.
    # a group leader of three years or more (the next rung), or a scientist of eight years or more (one skip, over the
    # project-lead rung), with published work
    LS_CHAIR: dict(req="~has('professor') & has('published research') & ((yrs_has('research group leader') >= 3) | "
                       "(yrs_has('research scientist') >= 8))"),
    # two years or more on a rung below the scientist's post (roles.py after=), with a degree
    LS_FAMOUS_LAB: dict(req="~has('research scientist') & has('graduate') & ((yrs_has('research assistant') >= 2) | "
                            "(yrs_has('laboratory technician') >= 2) | (yrs_has('research data steward') >= 2) | "
                            "(yrs_has('research software engineer') >= 2))"),
    # a new doctor in the first five years as a scientist (the postdoc's rung, the doctorate, is in roles.py rungs=)
    LS_FELLOWSHIP: dict(req="~has('postdoctoral researcher') & has('doctoral graduate') & "
                            "(yrs_has('research scientist') <= 5) & (age <= 45)"),
    # a research scientist of two years or more: the rung below every post the singles go for
    LS_CENTRE: dict(req="yrs_has('research scientist') >= 2"),
    # a volunteer of four years or more, citizen scientist or community observer (roles.py after= of the assistant)
    LS_SURVEY: dict(req="~has('research assistant') & ((yrs_has('citizen scientist') >= 4) | "
                        "(yrs_has('community observer') >= 4))"),
}
