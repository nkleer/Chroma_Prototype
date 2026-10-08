# Chroma content pack: Politics. Proposed engine conditions for the pack's two echoes, in the shape of
# earth_rules.PACK_RULES["science"]["ECHO"] (anchor at the time of the anchor moment; req, more, less when the echo
# comes). Plain data for the engine thread, which owns PACK_RULES and may reword anything. JUST is earth_rules.JUST.
JUST = 1 / 12
ECHO_POLITICS = {
    # a local fight, a protest or a bitter election that leaves the person wanting to stand (the door from the street)
    "the fight that made you want to stand": dict(
        anchor=f"had(['your town faces a change you could fight', 'a protest to save the local hospital', "
               f"'a sense of injustice', 'a bitter election', 'they ask you to lead because you stood up once'], {JUST})",
        req="~(has('local councillor') | has('mayor') | has('member of parliament')) & (age >= 18)",
        more=["has('activist in a cause')", "has('party member')", "(hW + hR) > .5"],
        less=["stress > 1.5", "health < .3"]),
    # a school debate, or a young campaigner's stand, back years later with time to spare (the door from the past)
    "the debate you never forgot": dict(
        anchor=f"had(['a debate or contest at school', 'defending a speaker you cannot stand'], {JUST}) & (age < 30)",
        req="(age >= 19) & (time > .4)",
        more=["retired", "kids_home == 0", "has('public speaking')"],
        less=["stress > 1.5", "money < .2"]),
}


# ---------------------------------------------------------------- long shots (merged 2026-10-06 with politics-longshots.lib)
# Chroma content pack: Politics. Proposed engine conditions for the long shots of politics-longshots.lib
# (chroma-packs/LONGSHOTS-BRIEF.md, sections 1 and 2): the two echoes in the shape of
# earth_rules.PACK_RULES["politics"]["ECHO"] (anchor at the time of the anchor moment; req, more, less when the echo
# comes), and the life events' gates in the shape of PACK_RULES["politics"]["LIFE"] (req, more, less). Merged
# 2026-10-06 with politics-longshots.lib and live since 10-06 19:37 Emren's time (16:37 UTC; batch.PACKS reads this file
# into PACK_RULES); round 5 (2026-10-07) adds the gate and anchor of 'the campaign loses its organiser' and two
# standings for the run for mayor. Plain data, nothing runs. JUST is earth_rules.JUST. Condition words only from
# batch.COND_VOCAB, the engine's ago_ clocks (engine.AGO: ago_fail_long), has(), was() and yrs_has() (engine.py,
# cond_ns); comparisons are in brackets, since & binds tighter than a comparison.
#
# Why each anchor has three parts (so the echo speaks of the right attempt):
#   has('a long shot that missed')   the shared perk (core/longshot.py), given by the engine after a real long shot;
#   had([...], JUST)                 one of the pack's long-shot moments was met within the last month;
#   (ago_fail_long < JUST)           a long shot failed within the last month (engine clock, 08:21: a failed act for a
#                                    title, or granting the perk, at true odds under .1), so a person who already held
#                                    the perk and took a safe option here anchors nothing.
# The long-shot options carry no `mark: took a wild risk`; since 07:56 the hospital echo needs a failed bodily act
# anyway (ago_fail_body), so a lost election is never told as a night in hospital.
#
# Round 2 (Emren, 09:18: "Big titles like parliament member needs consecutive steps ... commitment, and maybe
# consistency"): every long shot is a bold try at the next rung, or a skip of one rung by someone with years on the rung
# below. holds: says which names bring a person to the moment; the LIFE gates below say for how many years
# (yrs_has(), the years since the name was last gained, 0 when not held) and who may not come.
JUST = 1 / 12

# The moments whose miss is a long shot at a final rung, for the second try ({missed} is the title they were for):
# 'election night' (the seat, for a candidate with no party nomination, 50 x .04), 'polling day for mayor' (the chain,
# for a candidate who never sat on the council, 10; round 3: the run for mayor is now the step that gives the
# candidacy), the two long shots for party leader and head of government, and 'the leadership falls vacant' (party
# leader, 15 to 17 x .2 without reach). The second try is written at 12, above all of them.
_FINAL = ("['election night', 'polling day for mayor', 'a challenge from the back benches', "
          "'the campaign nobody gave a chance', 'the leadership falls vacant']")
# Every moment in the pack whose miss can be a long shot, for making peace with it: the above, a selection from
# outside the party ('a seat falls vacant', 12 x .1), and the career entry by letter (about 1 in 10).
# Round 5, 2026-10-07 (P9): and the campaign's own posts ('the campaign loses its organiser', 5); the letter is at 5 now
_ANY = ("['election night', 'a seat falls vacant', 'the leadership falls vacant', "
        "'polling day for mayor', 'a challenge from the back benches', "
        "'the campaign nobody gave a chance', 'writing in cold for a job in politics', "
        "'the campaign loses its organiser']")
_SPAN = 13   # years: the longest delay (12) and the anchor month, to tell which race the miss was in

ECHO_POLITICS_LONGSHOTS = {
    # the second try: years after a long shot at a final rung missed, the same race comes round again (rate .15 in the
    # .lib: about 1 anchor in 5 comes back, as about 1 losing candidate in 5 stands again; estimate). The singles give
    # {missed}, so req keeps it to the same miss and the same rung: no other long shot missed since the anchor (else
    # {missed} would be that later title), the seat still held for a missed leadership (a facet waits for its title),
    # and the lead still held for a missed government.
    "the race comes round again": dict(
        anchor=f"has('a long shot that missed') & had({_FINAL}, {JUST}) & (ago_fail_long < {JUST})",
        req=f"(age <= 80) & (health > .35) & (ago_fail_long >= sa) & "
            f"(~had(['a challenge from the back benches', 'the leadership falls vacant'], {_SPAN}) | "
            f"has('member of parliament')) & "
            f"(~had(['the campaign nobody gave a chance'], {_SPAN}) | has('party leader'))",
        more=["has('good name in town') | has('voice at the town hall') | has('a following in the party') | "
              "has('allies in the party')",
              "has('a loyal campaign team') | has('a list of supporters') | has('canvassing')",
              "time > .4"],
        less=["stress > 1.5", "money < .15", "ago_move < sa"]),
    # making peace with it: years after any long shot in the pack missed, what the attempt gave (rate .3: about 2
    # anchors in 5)
    "making peace with the long shot": dict(
        anchor=f"has('a long shot that missed') & had({_ANY}, {JUST}) & (ago_fail_long < {JUST})",
        req="age >= 25",
        more=["age >= 45", "retired | (kids_home == 0)", "ties > .5"],
        less=["stress > 1.5", "health < .3"]),
}

# Gates for the six life events with a gate (five, and L6 in round 5; PACK_RULES["politics"]["LIFE"], the same shape as
# earth_rules.LIFE: req, more, less; 'polling day for mayor' needs none: its holds: is the candidacy itself;
# batch.py reads LIFE for any moment named in it). holds: alone cannot say for how long a name was held, nor exclude:
# a party leader is also a member of parliament, a sitting mayor also has a good name in town.
# the five posts the letter asks for, and the seat: never for someone who already holds one (round 3: the rungs below,
# a branch office, a caseworker's post, a data analyst's, a salesperson's or a journalist's, are where the letter starts)
_IN_POLITICS = ("has('political adviser') | has('party official') | has('lobbyist') | has('policy analyst') | "
                "has('speechwriter') | has('member of parliament')")
# a local base held for years: the council or the mayoralty, a former seat, or a long-standing civic voice who also
# leads something in the town
_LOCAL_BASE = ("(yrs_has('local councillor') >= 4) | (yrs_has('mayor') >= 2) | has('former member of parliament') | "
               "((yrs_has('voice at the town hall') >= 6) & (has('activist in a cause') | has('union rep') | "
               "has('residents\\' committee member') | has('school-governance board member') | "
               "has('civil-liberties campaigner') | has('local hero')))")
# years of standing in the town outside the council: a party branch office, a civic post, a known local name, a
# business, or a community lead
# Round 5, 2026-10-07 (P4): a party member of six years and an activist of five may also be urged to run for mayor
# (the moment's holds: name them too), so [mayoral candidate] is met more widely at the same rate and chances
_TOWN_STANDING = ("(yrs_has('local party officer') >= 4) | (yrs_has('voice at the town hall') >= 5) | "
                  "(yrs_has('residents\\' committee member') >= 5) | (yrs_has('school-governance board member') >= 4) | "
                  "(yrs_has('union rep') >= 5) | (yrs_has('local hero') >= 5) | (yrs_has('good name in town') >= 10) | "
                  "(yrs_has('founder of a firm') >= 8) | (yrs_has('family business') >= 10) | "
                  "(yrs_has('party member') >= 6) | (yrs_has('activist in a cause') >= 5)")
# the rung below each post, held for years (round 3, engine check 11:18; roles.py after=): each single requires its
# own rung (without: impossible), and this gate asks for the years on at least one of them: party official from local
# party officer (1 year), policy analyst from data analyst (2, with a degree), lobbyist from salesperson (3),
# speechwriter from journalist (3), political adviser from constituency caseworker (1)
_POL_RUNG = ("(yrs_has('local party officer') >= 1) | (has('graduate') & (yrs_has('data analyst') >= 2)) | "
             "(yrs_has('salesperson') >= 3) | (yrs_has('journalist') >= 3) | (yrs_has('constituency caseworker') >= 1)")
LIFE_POLITICS_LONGSHOTS = {
    # the candidacy with no party: a real local base held for years; never a sitting member or a candidate already
    "standing with no party behind you": dict(
        req=f"~has('member of parliament') & ~has('parliamentary candidate') & ({_LOCAL_BASE})",
        more=["(yrs_has('local councillor') >= 8) | (yrs_has('mayor') >= 4)",
              "has('good name in town') | has('local hero') | has('a list of supporters') | has('a loyal campaign team')"],
        less=["has('party member')", "stress > 1.5", "money < .1"]),
    # a run for mayor from outside the council: years of standing in the town; never someone who sat on the council or
    # held the chain, nor a candidate already in the race (round 3: the run gives [mayoral candidate], and 'polling day
    # for mayor' decides)
    "a run for mayor from outside the council": dict(
        req=f"~was('local councillor') & ~was('mayor') & ~has('mayoral candidate') & ({_TOWN_STANDING})",
        more=["has('voice at the town hall') | has('local hero')", "ago_move > 10"],
        less=["ago_move < 3", "stress > 1.5"]),
    # a challenge from the back benches: four years or more in the seat, no ministry, not the leader
    "a challenge from the back benches": dict(
        req="(yrs_has('member of parliament') >= 4) & ~has('minister') & ~has('party leader')",
        more=["yrs_has('member of parliament') >= 8", "has('a following in the party') | has('allies in the party')"],
        less=["stress > 1.5"]),
    # the campaign nobody gave a chance: a party leader of two years or more, not already at the head of government
    "the campaign nobody gave a chance": dict(
        req="(yrs_has('party leader') >= 2) & ~has('head of government')",
        more=["has('known across the country')"],
        less=["stress > 1.5"]),
    # writing in for a job in politics: years on the rung below, and none of the five posts yet
    "writing in cold for a job in politics": dict(
        req=f"~({_IN_POLITICS}) & (age <= 70) & ({_POL_RUNG})",
        more=["has('graduate')", "has('friend in power') | has('mentor')", "time > .4"],
        less=["stress > 1.5"]),
    # Round 5, 2026-10-07 (P9): the campaign loses its organiser: a volunteer or branch officer of a year (holds:,
    # tenure:) who holds none of the three posts it offers, nor a post the letter asks for
    "the campaign loses its organiser": dict(
        req=f"(age <= 75) & ~has('campaign organiser') & ~has('constituency caseworker') & ~has('pollster') & "
            f"~({_IN_POLITICS})",
        more=["(yrs_has('campaign volunteer') >= 3) | (yrs_has('local party officer') >= 3)", "has('canvassing')"],
        less=["stress > 1.5", "time < .2"]),
}
