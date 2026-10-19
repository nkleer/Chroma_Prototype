# Chroma content pack: The Five Callings. Proposed engine conditions, in the shape of ../art/engine-conditions.py and
# earth_rules.PACK_RULES (ECHO: anchor at the time of the anchor moment; req, more, less when the echo comes; LIFE: who
# a life event can come to, read by batch.py as the moment's gate). Plain data for the Engine, which owns PACK_RULES
# (it pastes these with calib_v7/paste_pack_rules.py) and may reword anything. JUST is earth_rules.JUST. Every anchor
# names one of this pack's own moments or a condition the engine already reads. Pathways and packs thread, 2026-10-19
# (v24, switched off until `callings` is in batch.PACKS).
JUST = 1 / 12

# The rung below (Emren 10-06 09:18; engine 10:38): a life event that gives a career or a summit comes only to someone
# on the rung below it with a year or more on it (several for a summit), or one rung below that after years on it;
# never to a perk alone. The moment's holds: names the rungs; these gates add the exact years where one tenure: cannot
# say them.
LIFE_CALLINGS = {
    # W: the faith leader
    "the congregation needs a senior minister": dict(req="~has('senior cleric') & (age >= 35) & "
                                                         "((yrs_has('ordained religious minister') >= 6) | "
                                                         "(yrs_has('member of a monastic community') >= 8))"),
    "the order chooses its head": dict(req="~has('head of a faith order') & (age >= 45) & "
                                           "((yrs_has('senior cleric') >= 6) | "
                                           "(yrs_has('member of a monastic community') >= 15))"),
    # U: the inventor
    "the prototype works": dict(req="~has('inventor') & (has('prototyping') | has('fixing things')) & "
                                    "((yrs_has('software developer') >= 2) | (yrs_has('civil engineer') >= 2) | "
                                    "(yrs_has('machinist') >= 2) | (yrs_has('electrician') >= 2) | "
                                    "(yrs_has('founder of a firm') >= 1) | (yrs_has('apprentice') >= 2))"),
    "an invention in every home": dict(req="~has('celebrated inventor') & (yrs_has('inventor') >= 4)"),
    # B: the magnate
    "the board needs a chief executive": dict(req="~has('chief executive') & (age >= 28) & "
                                                  "((yrs_has('founder of a firm') >= 3) | (yrs_has('shop owner') >= 4) | "
                                                  "(yrs_has('café or bar owner') >= 4) | "
                                                  "(yrs_has('shift manager') >= 6))"),
    "a rival firm is for sale": dict(req="~has('magnate') & ((yrs_has('chief executive') >= 4) | "
                                         "(yrs_has('founder of a firm') >= 8))"),
    # R: the commander
    "officer selection": dict(req="~was('army officer') & (age >= 20) & (age <= 40) & ~has('someone with a record') & "
                                  "((yrs_has('soldier') >= 2) | has('graduate') | has('national service done'))"),
    "the army needs a new general": dict(req="~has('general') & (yrs_has('army officer') >= 12)"),
    # G: the healer
    "the ward needs someone in charge": dict(req="~has('senior nurse or midwife') & ((yrs_has('nurse') >= 4) | "
                                                 "(yrs_has('midwife') >= 4))"),
    "patients come from far away": dict(req="~has('renowned healer') & ((yrs_has('senior nurse or midwife') >= 4) | "
                                            "(yrs_has('midwife') >= 10) | (yrs_has('nurse') >= 12) | "
                                            "(yrs_has('physician') >= 10) | "
                                            "(yrs_has('complementary therapist') >= 12))"),
    # the world-only steps
    "the god speaks in the temple": dict(req="~has('head of a faith order') & ((yrs_has('senior cleric') >= 3) | "
                                             "(yrs_has('ordained religious minister') >= 10))"),
    "the guild commissions a flying ship": dict(req="~has('celebrated inventor') & ((yrs_has('inventor') >= 3) | "
                                                    "(yrs_has('civil engineer') >= 6) | (yrs_has('machinist') >= 6))"),
    "a seat among the merchant princes": dict(req="~has('magnate') & ((yrs_has('chief executive') >= 3) | "
                                                   "(yrs_has('founder of a firm') >= 6))"),
    "the war leader is chosen at the gathering": dict(req="~has('general') & (((yrs_has('army officer') >= 6) & (age >= 40)) | "
                                                          "(yrs_has('soldier') >= 12))"),
    "the sickness in the winter camp": dict(req="(yrs_has('nurse') >= 2) | (yrs_has('midwife') >= 2) | "
                                                "has('senior nurse or midwife')"),
}

# ---------------------------------------------------------------- long shots
# A long shot is a bold try at the next rung, or a skip of at most one rung by someone with years on the rung below
# (Emren 10-06 09:18). Every one-colour option at chance 1 to 5 that gives a title carries `grants_if_fails: a long
# shot that missed` (core/longshot.py). The echoes anchor on that perk, one of these moments within JUST, and the
# engine's clock ago_fail_long within JUST (set only by a real long-shot miss), so they speak of this attempt and not of
# a perk held from another pack. The second try offers `title: {missed}`.
LONGSHOTS_CALLINGS = ['a sermon that goes round the country', 'the garage invention',
                      'the market stall that became a chain', 'the field commission', 'the remedy that worked']
LIFE_CALLINGS_LONGSHOTS = {
    "a sermon that goes round the country": dict(
        req="~has('senior cleric') & (((yrs_has('ordained religious minister') >= 3) & (age >= 35)) | "
            "(yrs_has('lay religious teacher') >= 5) | (yrs_has('street preacher') >= 3))"),
    "the garage invention": dict(
        req="~was('inventor') & (has('fixing things') | has('prototyping')) & ((yrs_has('apprentice') >= 1) | "
            "(yrs_has('machinist') >= 1) | (yrs_has('electrician') >= 1) | (yrs_has('software developer') >= 1) | "
            "(yrs_has('repair-cafe volunteer') >= 2) | has('workshop'))"),
    "the market stall that became a chain": dict(
        req="~has('chief executive') & ((((yrs_has('shop owner') >= 2) | (yrs_has('café or bar owner') >= 2)) & (age >= 28)) | "
            "(yrs_has('shop assistant') >= 4))"),
    "the field commission": dict(
        req="~was('army officer') & (yrs_has('soldier') >= 3) & (age <= 45)"),
    "the remedy that worked": dict(
        req="~has('renowned healer') & ((yrs_has('nurse') >= 3) | (yrs_has('midwife') >= 3) | "
            "(yrs_has('complementary therapist') >= 3) | "
            "has('senior nurse or midwife'))"),
}
ECHO_CALLINGS_LONGSHOTS = {
    # the second try: years later the same kind of door opens a crack, and the try is for the same title again
    "the calling, years later": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_CALLINGS!r}, {JUST}) & (ago_fail_long < {JUST})",
        req="(age >= 20) & ~has('head of a faith order') & ~has('celebrated inventor') & ~has('magnate') & "
            "~has('general') & ~has('renowned healer')",
        more=["(hR + hB) > .5", "time > .4", "has('mentor') | has('old comrades') | has('investors who back you')"],
        less=["stress > 1.5", "money < .15", "health < .4"]),
    # making peace with it: the long shot becomes service at the rung the person holds, a pupil taught, a door held open
    "the long shot becomes a life of service": dict(
        anchor=f"has('a long shot that missed') & had({LONGSHOTS_CALLINGS!r}, {JUST}) & (ago_fail_long < {JUST})",
        req="(age >= 25) & ~has('head of a faith order') & ~has('celebrated inventor') & ~has('magnate') & "
            "~has('general') & ~has('renowned healer')",
        more=["sa > 10", "(hW + hG) > .5", "has('teaching') | has('mentor') | has(\"apprentice of one's own\")"],
        less=["stress > 1.5", "health < .3"]),
}
