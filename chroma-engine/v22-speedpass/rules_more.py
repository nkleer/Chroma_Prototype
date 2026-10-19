# rules_more.py: part 7 of 11 of earth_rules.py, the engine's reading of the Library's words.
# Later batches' moments and fixes.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# ---- next batch (Emren's point 11, the Library's drafts/next2): who one is drawn to and gender unease are found, never caused
# (attr 0-4 and unease are drawn at birth, engine identity); society moves when and how they are named
INNER.update({
    "a feeling for a friend that does not fit": dict(req="(attr >= 1) & (age >= 10)",
        more=["alive_friend > 0", "(age >= 11) & (age <= 14)"], less=["alive_friend == 0"]),
    "the clothes and the name that do not fit": dict(req="unease & (age >= 8)",
        more=["(age >= 11) & (age <= 16)"], less=[]),
    "the feeling is not going to pass": dict(req="(attr >= 2) & (age >= 13)",
        more=["had(['a feeling for a friend that does not fit'], 8)", "(age >= 16) & (age <= 19)"],
        less=["held_faith"]),
    "a late truth inside a marriage": dict(req="(attr >= 2) & ~mk('came out') & (age >= 35) & held_partner",
        more=["mk('kept it hidden')", "mk('gave in to pressure')", "female", "kids_home == 0", "ago_death < 2"],
        less=["held_faith"]),
    "a name that has waited for decades": dict(req="unease & ~mk('named their gender') & (age >= 30)",
        more=["kids_home == 0", "ago_death < 2", "retired", "mk('kept it hidden')"], less=["held_faith"]),
})
ECHO.update({
    # the law catches up with a wrong done months or years before
    "the police at the door": dict(anchor=f"mk('broke the law', {JUST})", req="True",
        more=["mkn('broke the law') >= 2", "has('someone with a record')"], less=["ago_move < sa"]),
    # after a failed risky act that put the person in hospital (the engine's near_death), or a failed night of drugs or risk
    "waking up in hospital": dict(
        anchor=f"(ago_near_death < {JUST}) | (mk('used drugs', {JUST}) & (ago_fail_big < {JUST})) | "
               f"(mk('took a wild risk', {JUST}) & (ago_fail_body < {JUST}))",   # a wild risk to the body, not an elopement (packs 07:52)
        req="True", more=["ago_near_death < .1"], less=["support > .6"]),
})

# gates for the rest of the next batch (the Library's drafts/next2/engine-gates.md, 22:30); everyday moments are gated
# the same way as life events (batch: any moment named in LIFE)
LIFE.update({
    # threshold seasons
    "the ring in the drawer since spring": dict(req="held_partner & ~has('engaged') & ~has('wife or husband')"),
    "the last of the old generation is buried": dict(req="(alive_parent == 0) | had(['a parent dies'], 1)"),
    "a flat in the sun near old friends": dict(req="has('homeowner')"),
    "the pill box with seven little doors": dict(
        req="(health < .45) | had(['living with a chronic illness', 'a heart attack or stroke'], 99)"),
    # a life taken: only where a violent partnership has gone on for years
    "the night it goes too far": dict(req="held_partner & (yrs_partner >= 2) & ((stress > 1) | (trouble > .5))"),
    # intimacy (adults only)
    "a match who wants to meet tonight": dict(
        req="(age >= 18) & ~held_partner & (((ago_end_partner >= 1) & (ago_end_partner < 99)) | (age >= 30))"),
    "your ex wants to try again": dict(req="(age >= 18) & ~held_partner & (ago_end_partner <= 3)"),
    "a friend says they are in love with you": dict(req="(age >= 18) & (alive_friend > 0)"),
    "single by choice, and everyone asks why": dict(req="(age >= 30) & ~held_partner & (ago_end_partner >= 2)"),
    "years together, and the bedroom has gone quiet": dict(req="(age >= 30) & held_partner & (yrs_partner >= 5)"),
    "desire and a body that is changing": dict(req="age >= 40"),
    "a late passion": dict(req="(age >= 50) & held_partner & (yrs_partner >= 10)"),
    "an invitation for three": dict(req="age >= 18"),
    "the last night of a work trip": dict(req="age >= 18"),
    # identity: only to the people it concerns
    "the first person you tell": dict(req="(attr >= 2) & ~mk('came out') & (age >= 14)"),
    "a love nobody can know about": dict(req="(attr >= 2) & (age >= 15)"),
    "telling the family who you are": dict(req="((attr >= 2) | unease) & (age >= 13)"),
    "everyone asks when you will settle down": dict(req="(attr >= 2) & ~mk('came out') & (age >= 16)"),
    "asking to be called by another name": dict(req="unease & (age >= 12)"),
    # pastimes
    "a first fish on a grandparent's line": dict(req="alive_grandparent > 0"),
    "dawn on the lake, alone with a rod": dict(more=["has('hunting and fishing') | has('fishing licence')"]),
    "teaching a grandchild to fish": dict(more=["has('hunting and fishing')"]),
    # risk
    "cocaine at the office party": dict(req="held_career"),
    "the last week of the painkillers": dict(
        req="had(['a serious accident or illness', 'an operation gives something back', 'an operation that makes things better', "
            "'a fall at home'], 1) | (ago_near_death < 1) | ((ago_fail_big < 1) & (heavy_risk > 0))"),
    "a racing heart after a heavy weekend": dict(req="hedon_n > 1.5"),   # pleasure-seeking acts made a habit, this past year
    "the cyclist at dusk": dict(req="has('car')"),
    "up the ladder to clear the gutters": dict(req="has('homeowner') & ~has('living in residential care')"),
    # title stages: a child of the right age in the character's care (years since the first child came)
    "the first night alone in charge": dict(req="held_children & (yrs_children < 6)"),
    "a week with no room left in it": dict(req="held_children & (yrs_children >= 5) & (yrs_children <= 16)"),
    "the child's new favourite grown-up": dict(req="held_children & (yrs_children < 18)"),
    "needed a little less each year": dict(req="held_children & (yrs_children >= 10)"),
})
# ---- release N1c (the Library's drafts/new3/earth-identity-roles.lib, its "# gate:" lines): the role the world expects,
# and the rare lives of sex and gender; found, never caused (cross_title, unease, intersex, ace and partner_same come
# from the engine's identity block; with it off they are all False and these moments never come)
INNER.update({
    "the only one of your kind at work": dict(req="cross_title & (age >= 18)",
        more=["role_strict > .5"], less=["role_strict < .2"]),
    "starting treatment to live as yourself": dict(req="unease & mk('named their gender') & (age >= 18)",
        more=["accept_trans > .6", "money > .5", "trans"], less=["accept_trans < .3", "money < .25"]),
    "the word the doctors used for your body": dict(req="intersex & (age >= 9)",
        more=["(age >= 11) & (age <= 14)"], less=[]),
    "everyone else feels something you do not": dict(req="ace & (age >= 15)",
        more=["(age >= 17) & (age <= 23)", "alive_friend > 0"], less=["held_faith"]),
    # moving into care within the year, or carers coming to the home (health below .4)
    "growing old without hiding again": dict(
        req="(mk('came out') | mk('named their gender')) & (age >= 70) & "
            "((has('living in residential care') & (yrs_has('living in residential care') < 1)) | (health < .4))",
        more=["accept_trans < .3", "~held_partner & ~held_children"], less=["held_partner"]),
})
LIFE.update({
    "who stays home with the baby": dict(req="held_partner & held_children & (yrs_children < 1)"),
    "a child of your own, another way": dict(req="partner_same & ~held_children & (age >= 25) & (age <= 45)"),
})
LIFE.update({   # live moments the Library's writers found ungated (engine-gates.md, 22:45)
    "your pet dies": dict(req="had(['a pet of your own'], 99) | has(\"dog of one's own\") | has(\"cat of one's own\")"),
    "sharing a room with your sibling": dict(req="alive_sibling > 0"),
    "the last slice of birthday cake": dict(req="alive_sibling > 0"),
    # hobbies spaced out for everyone (gap 2-4); likelier for those who practise them (the gap still holds)
    "an away match in the rain": dict(more=["has('club member') | has('on the team')"]),
    "the knitting circle at the library": dict(more=["has('sewing and mending')"]),
})
FIXES.update({
    "the last day at work": dict(retires=True),   # the career ends here, as retirement (engine retire_season)
    # its gate (retired within the year) already says no work; the engine reads excludes: career as 'neither working nor
    # retired' (the job-seeking sense), which shut it out for every retiree (Library 23:20)
    "the first months of retirement": dict(excludes=None),
    "twenty-five years together": dict(once=True),   # once per partnership (it needs: partner, so a new one opens it again)
})

