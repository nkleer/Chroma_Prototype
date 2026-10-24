# rules_moments.py: part 1 of 11 of earth_rules.py, the engine's reading of the Library's words.
# Inner moments, echoes, readings, the child versions, life-event gates, FIXES.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
# a person is "in a hard stretch" or "in need" (used by several echoes)
NEED_NOW = "(trouble > .3) | (ago_hard < .5) | (money < .25) | (belonging < .35) | (ago_loss < .5)"

INNER = {
    "the same week, over and over": dict(
        req="(quiet >= 12) & ((meaning < .45) | (flat_comp >= 12))",
        more=["juvenile | young_adult", "autonomy < .4", "retired & (n_plan == 0)", "hR > .3", "held_career & (yrs_career > 3)"],
        less=["(n_passion > 0) | (n_plan > 0)", "(ago_child < 1) | (ago_job < 1) | (ago_move < 1)", "steady > .6"]),
    "a friend's good news stings": dict(
        req="(competence < .5) & (ties > .2)",
        more=["juvenile | young_adult", "competence < .35", "hB > .3"],
        less=["age > 50", "satisfaction > .65"]),
    "guilt that will not go away": dict(
        req="(mk('broke your word', 1) | mk('hid a wrong', .5) | mk('refused someone in need', 1)) & (lo_peace >= 4) & ~mk('owned up', .5)",
        more=["hW + hG > .45", "react > 1", "held_faith"],
        less=["mk('owned up', 2)", "hB > .3"]),
    "shame after a public failure": dict(
        req="(ago_fail_big < 1 / 12) & ((competence < .4) | (belonging < .4))",
        more=["react > 1.2", "hW > .3", "juvenile", "outlook < .4"],
        less=["(ties > .6) & (belonging > .6)", "steady > .6"]),
    "the itch to be somewhere else": dict(
        req="((ago_move > 5) & (ago_commit > 5) & ((autonomy < .45) | (meaning < .45))) | decade_edge | had(['a close friend moves away'], 1)",
        more=["age_mod == 9", "hR + hB > .45", "had(['the children leave home'], 1)", "freedom > .6"],
        less=["(ago_commit < 1) | (ago_child < 1)", "hW + hG > .45", "money < .2"]),
    "running on empty": dict(
        req="(hi_stress >= 12) & (time < .2) & ((autonomy < .4) | (cload > .3))",
        more=["held_career & kids_home", "hW > .3", "hU > .3"],
        less=["autonomy > .6", "ties > .6", "satisfaction > .65"]),
    "the anniversary of a death": dict(
        req="(ago_death >= 1) & (ago_death < 30) & chance(.25)",
        more=["ago_death < 4", "widowed", "belonging < .4", "ties < .3"],
        less=["ago_death > 10", "held_faith", "ties > .6"]),
    "nothing seems to matter": dict(
        req="(vlo_meaning >= 8) | (((ago_goal_end < 1) | (ago_retire < 1) | had(['the children leave home'], 1)) & (meaning < .45))",
        more=["young_adult | elder", "decade_edge", "ago_end_faith < 3", "eB > .3", "base_mood < .45"],
        less=["belonging > .6", "held_faith | held_community", "held_children", "held_career & (meaning > .6)"]),
    "homesick": dict(
        req="(ago_move < .25) & (belonging < .45)",
        more=["n_moves <= 1", "react > 1.2", "ties > .5"],
        less=["n_moves > 2", "held_partner"]),
    "anger that keeps building": dict(
        req="(fails13 >= 3) & (stress > 1) & (peace < .4)",
        more=["health < .5", "hR + hB > .45", "react > 1.2", "mk('made an enemy', 3)"],
        less=["steady > .6", "hW + hU > .45"]),
    "a craving that keeps calling": dict(
        req="hedon_n >= 8",
        more=["stress > 1.5", "time < .15", "hR + hB > .45"],
        less=["(n_plan > 0) | (n_passion > 0)", "held_partner | held_children"]),
    "trapped by a promise": dict(
        req="((bind_m > .2) | (yrs_any >= 1)) & (lo_auto >= 8)",
        more=["hR + hB > .45", "money < .25", "held_community | held_faith", "kids_home"],
        less=["money > .6", "ties > .6", "meaning > .6", "eW > .3"]),
    "jealousy in love": dict(
        req="(held_partner | (juvenile & had(['falling in love'], .25))) & ((belonging < .5) | betrayed) & chance(.3)",
        more=["betrayed", "ties < .3", "react > 1.2", "juvenile | young_adult"],
        less=["(yrs_partner >= 5) & (ties > .6)", "steady > .6"]),
    "feeling invisible": dict(
        req="((lo_belong >= 6) & (ties > .3)) | ((ago_retire < 1) & (ties < .4))",
        more=["elder", "ago_move < 1", "react < .8"],
        less=["held_children | held_community", "ties > .6", "hR > .3"]),
    "a sense of injustice": dict(
        req="(fails13 >= 2) | (era > .3)",
        more=["eW > .3", "outlook > .45", "juvenile | young_adult"],
        less=["money > .7", "outlook < .3", "hG > .3"]),
    "feeling old": dict(
        req="((health < .5) & (age >= 40)) | (round_birthday & (age >= 40)) | (ago_death < 1) | had(['your first grandchild'], 1)",
        more=["health < .5", "retired & (ago_retire < 2)", "outlook < .4"],
        less=["health > .8", "hG > .3", "held_community"]),
    "wanting to be noticed": dict(
        req="((belonging < .45) | (competence < .45)) & (ago_hard_win > 8 / 52)",
        more=["juvenile", "hB + hR > .45"],
        less=["held_children | held_community", "ago_win < 1 / 12", "hG > .3", "steady > .6"]),
    "longing for a child": dict(
        req="(~held_children | (yrs_children >= 5)) & ((meaning < .6) | (belonging < .6))",
        more=["yrs_partner >= 2", "eG + eW > .45", "(age >= 28) & (age <= 38)"],
        less=["time < .2", "money < .2", "hB + hR > .45", "ago_breakup < 1"]),
    "longing for love": dict(
        req="~held_partner & (ago_end_partner >= 1) & (belonging < .5)",
        more=["young_adult", "decade_edge", "widowed", "hR > .3"],
        less=["ago_breakup < .5", "belonging > .65"]),
    "the urge to protect": dict(
        req="(held_children | (alive_sibling > 0) | ((alive_parent > 0) & (age > 40))) & (ties > .5)",
        more=["kids_home", "hG + hW > .45", "react > 1.2"],
        less=["stress > 2", "ties < .4"]),
    "needing to be alone": dict(
        req="(lo_time >= 4) & (stress > 1) & (kids_home | held_partner | (stage <= 1))",
        more=["kids_home", "hU + hG > .45"],
        less=["belonging < .35", "hR > .3"]),
    "pride after a success": dict(
        req="ago_hard_win < 2 / 52",
        more=["child | juvenile", "hB + hW > .45"],
        less=["hG > .3"]),
    "a curiosity that will not let go": dict(
        req="(safety >= .45) & (competence >= .45) & (time > .3) & chance(.4)",
        more=["child", "belonging > .6", "hU > .3", "ago_move < 1"],
        less=["stress > 1.5", "money < .2"]),
    "ambition wakes up": dict(
        req="(competence > .55) & (ago_win < 1 / 12) & (satisfaction < .7)",
        more=["young_adult", "hB + hU > .45"],
        less=["had(['burnout'], 1)", "hG > .3", "elder", "kids_home & (yrs_children < 1)"]),
    "the urge to make something": dict(
        req="(time > .3) & ((ago_le < 1 / 12) | (abs(mood) > .2) | ((autonomy > .5) & (quiet >= 12)) | chance(.15))",
        more=["child | retired", "hR + hU > .45", "time > .5"],
        less=["time < .15"]),
    "a burst of energy": dict(
        req="((ok_body >= 3) | (bodyhab_n >= 3)) & chance(.3)",
        more=["child | juvenile", "hR + hG > .45"],
        less=["health < .5", "time < .15", "stress > 1.5"]),
    "gratitude": dict(
        req="(peace > .4) & ((ago_win < 2 / 52) | (support > .6) | had(['a narrow escape', 'a stranger saves you, or you save one', 'an operation gives something back'], 2 / 52) | chance(.15))",
        more=["hW + hG > .45", "age > 50", "held_faith"],
        less=["hB > .3", "stress > 2"]),
    "a quiet contentment": dict(
        req="(ok_needs >= 12) & (quiet >= 12) & (stress < .6) & (satisfaction > .6)",
        more=["age > 50", "(money > .5) & (ties > .5)", "hG + hW > .45"],
        less=["hR + hB > .45"]),
    "hope after a hard time": dict(
        req="(ago_hard < 1) & (easing >= 6)",
        more=["outlook > .45", "ties > .5", "held_faith"],
        less=["outlook < .3", "money < .15", "base_mood < .4"]),
    "inspiration strikes": dict(
        req="(time > .25) & (stress < 1.5) & chance(.3)",
        more=["hU + hR > .45", "n_passion > 0"],
        less=["outlook < .3", "health < .4"]),
    "awe": dict(
        req="(stress < 1.5) & chance(.25)",
        more=["held_faith", "child | elder", "hG + hU > .45"],
        less=["time < .15"]),
    "an old song brings it all back": dict(
        req="((belonging < .55) | (meaning < .55) | (age > 50)) & chance(.3)",
        more=["belonging < .4", "ago_move < 1", "elder", "hG + hW > .45"],
        less=["satisfaction > .75", "hR > .3"]),
    # C5's rare founding (Library PR #26, earth-world-institutions.lib). "founding" (the world's movement founding event
    # in the person's place this year, with a free movement slot) is False unless C5's movement slots are on (c5_faith,
    # world.py), so the moment never comes without them. Reach: ties in about the top tenth.
    # The spheres' haunt choices (item 15, N1; Library #49, earth-spheres-gathering.lib), once at each new life stage
    # with 4 or more free hours a week. "haunts" is False until phase 2's haunts are built, so they never come before.
    **{nm_: dict(req="haunts & (time > .2)", more=["belonging < .5", "ties < .4"], less=["time < .3", "health < .3"])
       for nm_ in ("where the evenings go at fifteen", "where the evenings go at twenty", "where the evenings go at thirty",
                   "where the days go at sixty-five")},
    "a following of your own": dict(
        # v25: the Library's "unmet meaning high (below .4 for a year)" read on the v7 needs table, where adult meaning sits
        # above .95 in half of all weeks and a year below .5 never came (the moment came 0 times in 800 lives left alone),
        # and ten years of faith with wide ties keeps it higher still: meaning in the lowest quarter of adult weeks (< .9)
        # while the founding's year-long window is open
        req="founding & (meaning < .9) & (ties > .8) & (yrs_faith >= 10)",
        more=["outlook > .55", "ties > .9", "hW + hU > .5"],
        less=["harsh > .5", "ties < .85"]),
}
# with founder_moment off (K4: v23.2's lives), the req each of these had before v25 (batch: the condition's req_off)
INNER_V25_OFF = {"a following of your own": "founding & (meaning < .4) & (lo_meaning >= 52) & (ties > .8) & (yrs_faith >= 10)"}

# echoes: anchor starts the clock (checked monthly; a mark "within the last month" means it was just made)
JUST = 1 / 12
ECHO = {
    "a promise you broke comes back": dict(anchor=f"mk('broke your word', {JUST})", req="True",
        more=["ago_move > sa", "ties > .6"], less=["ago_move < sa", "mk('owned up', sa)"]),
    "a promise kept for years pays off": dict(anchor=f"mk('kept your word', {JUST}) & (mkn('kept your word') >= 2)", req="True",
        more=["ago_move > sa"], less=["ago_move < sa"]),
    "someone you helped returns the favour": dict(anchor=f"mk('helped someone in need', {JUST})", req=NEED_NOW,
        more=["ties > .5", "ago_move > sa"], less=["ago_move < sa"]),
    "the one you turned away is the one who can help": dict(anchor=f"mk('refused someone in need', {JUST})", req=NEED_NOW,
        more=["ago_move > sa"], less=["ago_move < sa"]),
    "an old enemy holds the keys": dict(anchor=f"mk('made an enemy', {JUST})", req="held_career | held_community",
        more=["ago_move > sa", "held_career & (yrs_career > sa)"], less=["ago_move < sa"]),
    "an old friend turns up when you need one": dict(anchor=f"mk('made a friend', {JUST})", req=NEED_NOW + " | (ago_move < .5)",
        more=["ago_hard < .5", "ago_death < .5"], less=[]),
    "the office you defied remembers": dict(anchor=f"mk('defied an authority', {JUST})", req="True",
        more=["ago_move > sa"], less=["ago_move < sa"]),
    "they ask you to lead because you stood up once": dict(anchor=f"mk_ok('defied an authority', {JUST})", req="True",
        more=["ago_move > sa"], less=["ago_move < sa"]),
    "the same pressure, again": dict(anchor=f"mk('gave in to pressure', {JUST})", req="True",
        more=["ago_move > sa", "autonomy < .4"], less=["ago_move < sa"]),
    "you catch someone doing what you once did": dict(anchor=f"mk_ok('hid a wrong', {JUST})", req="held_children | held_career",
        more=["kids_home", "held_career & (yrs_career > 5)"], less=[]),
    "years of practice are noticed": dict(anchor=f"mk('learned a skill', {JUST})",
        req="(mkn('learned a skill') >= 3) & (mk_span('learned a skill') >= 10)",
        more=["n_passion > 0", "held_community"], less=["ties < .3"]),
    "a gamble that paid asks for another": dict(anchor=f"mk_ok('took a wild risk', {JUST})", req="True",
        more=["money > .5", "freedom > .5"], less=["kids_home", "time < .2"]),
    "the body remembers the wild years": dict(anchor=f"mk('took a wild risk', {JUST}) & (heavy_risk >= 2)", req="age >= 30",
        more=["heavy_risk >= 4", "health < .6"], less=["health > .85"]),
    "the home you left has changed": dict(anchor=f"mk_ok('left home', {JUST})", req="True",
        more=["alive_parent < 2"], less=[]),
    "the place you stayed needs you now": dict(
        anchor=f"mk('stayed home', {JUST}) | ((age >= 30) & (age < 30 + {JUST}) & (n_moves == 0) & ~mk('left home') & ~mk('moved away'))",
        req="n_moves == 0", more=["held_community"], less=["ties < .3"]),
    "roots call the one who moved away": dict(anchor=f"mk_ok('moved away', {JUST})",
        req="((alive_parent > 0) | (alive_sibling > 0)) & ~mk('came home', sa)",
        more=["alive_sibling == 0", "~kids_home"], less=["kids_home & held_partner"]),
    "the same chance comes round again": dict(anchor=f"mk('turned down a chance', {JUST})", req="True",
        more=["~kids_home"], less=["ago_move < sa"]),
    "you never learned to swim": dict(anchor=f"(age >= 18) & (age < 18 + {JUST}) & chance(.15)",
        req="held_children | held_partner", more=["kids_home"], less=["health < .4"]),
    "the apology that was never made": dict(
        anchor=f"mk('hid a wrong', {JUST}) | mk('broke your word', {JUST}) | mk('made an enemy', {JUST})",
        req="~mk('owned up', sa)", more=["hB + hW > .45"], less=["ties < .3"]),
    "words that were never said": dict(anchor=f"(age >= 20) & (age < 20 + {JUST})",
        req="((alive_parent > 0) & (age > 45)) | (held_partner & (age > 65))", more=["hU + hG > .45"], less=["hR > .3"]),
    "a late chance to see the world": dict(
        anchor=f"(age >= 50) & (age < 50 + {JUST}) & (n_moves == 0) & ~mk('left home') & ~mk('moved away')",
        req="~kids_home & (retired | (age > 60)) & (money > .3)", more=["money > .5"], less=["health < .5", "money < .4"]),
    "someone younger does what you always planned": dict(
        anchor=f"(age >= 35) & (age < 35 + {JUST}) & ~mk('took a wild risk')", req="True",
        more=["n_plan > 0", "n_dream > 0"], less=["n_moves > 2"]),
    "twenty-five years together": dict(anchor=f"held_partner & (yrs_partner < {JUST})", req="held_partner & (yrs_partner >= 25)",
        more=["held_children"], less=["cload > .3", "health < .4"]),
    "among the faith you left": dict(anchor=f"ago_end_faith < {JUST}", req="True",
        more=["alive_parent > 0"], less=[]),
    "your words in your child's mouth": dict(anchor=f"held_children & (yrs_children < {JUST})", req="held_children & (yrs_children >= 20)",
        more=["ties > .5"], less=["ties < .3"]),
    "someone faces what you came through": dict(
        anchor=f"had(['a serious accident or illness', 'divorce after twenty years', 'losing your job', 'a parent dies', 'your partner dies', "
               f"'a heart attack or stroke', 'financial ruin', 'a breakup', 'living with a chronic illness', 'a frightening diagnosis'], {JUST})",
        req="True", more=["ties > .5"], less=["wound > .5"]),
    "lean times, again": dict(anchor=f"had(['money runs out at home', 'losing your job', 'financial ruin'], {JUST})", req="money < .3",
        more=["harsh > 0"], less=["money > .5"]),
    "every hour belongs to someone else": dict(anchor="hW >= .4", req="hW >= .35", more=["kids_home | held_community"], less=["~held_partner & ~held_children"]),
    "the notebooks come together": dict(anchor="hU >= .4", req="hU >= .35", more=["time > .4", "n_passion > 0"], less=["time < .15"]),
    "a cushion of your own": dict(anchor="hB >= .4", req="(hB >= .35) & (money > .4)", more=["harsh > 0", "era > .3"], less=[]),
    "all stories and no savings": dict(anchor="hR >= .4", req="(hR >= .35) & (money < .45)", more=["round_birthday"], less=["held_partner & (money > .3)"]),
    "everything rested on the one thing": dict(anchor="hG >= .4", req="(hG >= .35) & (held_career | held_community)", more=["harsh > 0"], less=[]),
}

# outside events read through the person's colors: when they come (timing.gap_years is the Library's), and for whom
READ = {
    "a festival comes to town": dict(more=["held_community", "prosper > 0"], less=["unrest > 0", "money < .2"]),
    "praise from a stranger": dict(more=["n_passion > 0", "held_career"], less=["ties < .3"]),
    "an unexpected refund or prize": dict(),
    "a wedding invitation from near strangers": dict(more=["ties > .6", "held_community"], less=["ties < .3"]),
    "a relative's success": dict(more=["alive_sibling >= 2", "prosper > 0"], less=["alive_sibling == 0", "harsh > 0"]),
    "the neighbours are doing well": dict(more=["prosper > 0"], less=["harsh > 0"]),
    "the new thing everyone is talking about": dict(more=["juvenile | young_adult", "money > .5"], less=["elder", "money < .2"]),
    "a national celebration": dict(less=["unrest > 0"]),
    "new people move in next door": dict(more=["ago_move < 3"], less=["(n_moves == 0) & (age > 40)"]),
    "a story about someone like you": dict(),
    "the sun goes dark at noon": dict(),
    "the home team wins the cup": dict(more=["held_community"]),
    "a snow day": dict(),
    "the first warm day of the year": dict(),
    "a pandemic and a lockdown": dict(more=["~held_partner & ~kids_home"]),
    "a recession": dict(more=["held_career & (money < .4)"], less=["retired", "money > .7"]),
    "a disaster in the next town": dict(more=["harsh > 0"]),
    "a war on the news": dict(more=["unrest > 0"]),
    "a bitter election": dict(more=["unrest > 0", "harsh > 0"]),
    "a wave of layoffs at work": dict(req="held_career", more=["harsh > 0"], less=["prosper > 0"]),
    "the local hospital is closing": dict(more=["harsh > 0"], less=["prosper > 0"]),
    "a scandal in the congregation": dict(req="held_faith | held_community"),
    "break-ins on the street": dict(more=["money < .3", "harsh > 0"]),
    "a rumour about you": dict(more=["held_career | held_community", "mk('made an enemy', 5)"], less=["ties < .3"]),
    "an insult from a stranger": dict(),
    "a bill you did not expect": dict(more=["money < .3"], less=["money > .7"]),
    "a heatwave": dict(more=["elder", "money < .3"]),
    "a run of bad luck": dict(more=["stress > 1", "harsh > 0"], less=["stress < .5"]),
}

# life events: gates the per_year rates assume but the batch cannot state in its own fields

# child versions (the Library's fix 9, staged 07:18): conditions proposed by the Library, checked by the engine
INNER_CHILD = {
    "bored on a rainy afternoon": dict(
        req="(quiet >= 4) & ((meaning < .75) | (autonomy < .7)) & chance(.3)",
        more=["alive_sibling == 0", "autonomy < .4", "hR > .3"], less=["n_passion > 0", "belonging > .8", "hU > .3"]),
    "a friend's new bike stings": dict(
        req="((competence < .6) | (belonging < .6)) & chance(.3)",
        more=["money < .12", "alive_sibling >= 1", "hB > .3"],
        less=["satisfaction > .65", "had(['someone was kind when it counted'], 1 / 12)", "hG > .3"]),
    "a fib that will not stop nagging": dict(
        req="(mk('hid a wrong', .25) | mk('broke your word', .25)) & ~mk('owned up', .25) & (lo_peace >= 2)",
        more=["hW + hG > .45", "react > 1"], less=["hB > .3", "mk('owned up', 1)"]),
    "everyone laughed when you got it wrong": dict(
        req="((fails13 >= 1) | (ago_fail_big < 1 / 12)) & ((competence < .5) | (belonging < .5))",
        more=["react > 1.2", "hW > .3", "outlook < .4"], less=["belonging > .8", "steady > .6"]),
    "an empty chair on a special day": dict(
        req="(((ago_death >= 1) & (ago_death < 8)) | (had(['your pet dies'], 5) & ~had(['your pet dies'], 1))) & chance(.25)",
        more=["ago_death < 3", "belonging < .5"], less=["held_faith", "belonging > .8", "(ago_death > 5) & (ago_death < 99)"]),
    "a temper that keeps boiling over": dict(
        req="((fails13 >= 2) | ((alive_sibling > 0) & chance(.3))) & (stress > .8) & (peace < .5)",
        more=["health < .5", "hR + hB > .45", "react > 1.2", "mk('made an enemy', 1)"], less=["steady > .6", "hW + hU > .45"]),
    "the dark at the top of the stairs": dict(
        req="((safety < .5) | (stress > .8) | had(['a thunderstorm at night'], 1 / 12) | (ago_move < 1 / 12)) & chance(.4)",
        more=["age < 8", "react > 1.2", "ago_move < .5"], less=["steady > .6", "age > 9"]),
    "a new baby takes up all the room": dict(
        req="(younger_siblings > 0) & (age < 10) & chance(.05)",   # only a child who gets a younger one (Library next3)
        more=["belonging < .5", "react > 1.2"], less=["alive_sibling >= 2", "steady > .6"]),
    "nobody watches the cartwheel": dict(
        req="(((belonging < .45) | (competence < .45)) & (ago_hard_win > 8 / 52)) | ((alive_sibling > 0) & (belonging < .5))",
        more=["hB + hR > .45"], less=["ago_hard_win < 1 / 12", "hG > .3", "steady > .6"]),
    "standing up for someone smaller": dict(
        req="((alive_sibling > 0) | (alive_friend > 0)) & (belonging > .5) & chance(.3)",
        more=["hG + hW > .45", "react > 1.2"], less=["stress > 2"]),
    "the glow of a gold star": dict(req="ago_hard_win < 2 / 52", more=["hB + hW > .45"], less=["hG > .3"]),
    "a question that will not go to bed": dict(
        req="(safety >= .45) & (time > .3) & chance(.2)",
        more=["belonging > .6", "hU > .3", "ago_move < 1"], less=["stress > 1.5", "money < .12"]),
    "an itch to build something": dict(
        req="(time > .3) & ((abs(mood) > .2) | (quiet >= 8)) & chance(.15)",
        more=["hR + hU > .45", "time > .5"], less=["stress > 1.5"]),
    "too much fizz to sit still": dict(
        req="((ok_body >= 3) | (bodyhab_n >= 3)) & chance(.3)",
        more=["hR + hG > .45"], less=["health < .5", "stress > 1.5"]),
    "someone was kind when it counted": dict(
        req="(peace > .4) & ((support > .6) | (ago_win < 2 / 52) | chance(.15))",
        more=["hW + hG > .45", "held_faith"], less=["hB > .3", "stress > 2"]),
    "more stars than anyone could count": dict(
        req="(stress < 1.5) & chance(.15)", more=["held_faith", "hG + hU > .45"], less=["time < .15"]),
}
READ_CHILD = {
    "snow closes the school": dict(),
    "the fair comes to town": dict(more=["prosper > 0"], less=["unrest > 0", "money < .2"]),
    "the teacher reads your work out to the class": dict(more=["competence > .55"]),
    "a wobbly tooth comes out": dict(),
    "the school trip": dict(less=["money < .2", "harsh > 0"]),
    "a new baby next door": dict(),
    "the summer holidays begin": dict(),
    "the lights go out on a winter night": dict(more=["harsh > 0"]),
    "a party you were not invited to": dict(more=["belonging < .5", "ago_move < 1"], less=["belonging > .8"]),
    "the old tree comes down in the storm": dict(more=["harsh > 0"]),
    "a scary story on the news": dict(more=["unrest > 0", "harsh > 0"]),
    "your favourite teacher is leaving": dict(),
    "lost for a few minutes at the shops": dict(),
    "in bed with a fever while the others play": dict(more=["health < .6"]),
}
INNER.update(INNER_CHILD)
READ.update(READ_CHILD)

# second child set (the Library, staged 08:14), with its fixes to the first set's likelier and rarer lines
INNER_CHILD_2 = {
    # ---- trouble
    "the first night away from home": dict(
        req="((safety < .78) | (ago_move < 1)) & chance(.2)",
        more=["age < 9", "react > 1.1", "ago_move < .5"], less=["steady > .15", "age > 10", "hR > .22"]),
    "voices raised downstairs after bedtime": dict(
        req="((stress > .75) | (money < .13) | had(['your parents split up'], 2)) & chance(.15)",
        more=["money < .12", "react > 1.1", "peace < .35"], less=["steady > .15", "belonging > .75"]),
    "nobody to play with at break time": dict(
        req="((belonging < .55) | (ago_move < 1)) & chance(.4)",
        more=["alive_sibling == 0", "react > 1.1", "ago_move < .5"], less=["belonging > .75", "hR > .22"]),
    "the sibling who always gets more": dict(
        req="(alive_sibling > 0) & ((belonging < .65) | (autonomy < .7)) & chance(.25)",
        more=["alive_sibling >= 2", "hB + hR > .42", "react > 1.1"], less=["steady > .15", "hG > .22"]),
    "the same bad dream again": dict(
        req="((stress > .85) | (ago_death < .5) | (ago_move < 1 / 12)) & chance(.35)",
        more=["age < 8", "react > 1.1", "safety < .65"], less=["steady > .15", "age > 9"]),
    # ---- mixed
    "a dare from the big kids": dict(
        req="(age >= 7) & ((belonging < .7) | (hR > .21)) & chance(.2)",
        more=["hB + hR > .42", "react > 1.1", "belonging < .5"], less=["steady > .15", "hW > .22"]),
    "in a hurry to be grown up": dict(
        req="(age >= 8) & ((autonomy < .75) | (alive_sibling > 0)) & chance(.15)",
        more=["hB + hR > .42", "age > 10", "freedom < .1"], less=["hG > .22", "steady > .15"]),
    "a secret that wants to burst out": dict(
        req="(alive_grandparent > 0) & (belonging > .55) & chance(.15)",
        more=["hW + hG > .42", "support > .4"], less=["stress > 1.2", "belonging < .45"]),
    "the lessons get hard": dict(
        req="((competence < .62) | (flat_comp >= 8)) & chance(.2)",
        more=["hR + hB > .42", "peace < .35", "time < .66"], less=["ago_hard_win < 1 / 12", "steady > .15"]),
    "a best friend finds a new best friend": dict(
        req="(alive_friend > 0) & (belonging < .7) & chance(.2)",
        more=["had(['a new kid joins your class'], .5)", "react > 1.1", "alive_sibling == 0"],
        less=["belonging > .75", "steady > .15"]),
    "saving up for something big": dict(
        req="(had(['your first pocket money'], 8) | (money > .14)) & chance(.12)",
        more=["money < .14", "hB + hW > .42", "had(['your first pocket money'], 1)"], less=["stress > 1.2", "ago_move < .5"]),
    # ---- joy
    "the morning things feel better": dict(
        req="((ago_death < .5) | (ago_fail_big < .5) | (ago_move < .5)) & (easing >= 3)",
        more=["support > .4", "hG + hW > .42"], less=["stress > 1.2"]),
    "a hero to be like": dict(
        req="(meaning > .72) & chance(.15)",
        more=["hR + hB > .42", "time > .65", "ago_win < 1"], less=["stress > 1.2", "outlook < .2"]),
    "a den of your own": dict(
        req="(time > .6) & (autonomy > .6) & chance(.1)",
        more=["hG + hR > .42", "alive_sibling > 0", "quiet >= 4"], less=["stress > 1.2", "ago_move < .25"]),
    "a promise kept all week": dict(
        req="(alive_grandparent > 0) & (safety > .6) & chance(.12)",
        more=["hW + hG > .42", "mk('kept your word', 2)"], less=["mk('broke your word', 1)", "stress > 1.2"]),
    "trusted with a grown-up job": dict(
        req="(age >= 7) & (autonomy > .7) & (safety > .6) & chance(.3)",
        more=["mk('kept your word', 2)", "hW + hB > .42"], less=["mk('hid a wrong', 1)", "mk('broke your word', 1)"]),
}
READ_CHILD_2 = {
    # ---- joys
    "your birthday party": dict(less=["money < .12", "ago_move < .25"]),
    "a week with the grandparents": dict(req="alive_grandparent > 0", more=["alive_grandparent >= 3"]),
    "fireworks night": dict(less=["harsh > 0", "unrest > 0"]),
    "the Saturday team wins at last": dict(req="(had(['sports day', 'tryouts for the team'], 1) & (competence > .55)) | (bodyhab_n >= 2)",
                                           more=["competence > .65"]),   # engine: no club yet, so a sporty child stands in
    "a parcel just for you": dict(more=["alive_grandparent >= 3"]),
    "a day out at the zoo": dict(less=["money < .12", "harsh > 0"]),
    "something lost turns up": dict(),
    # ---- troubles
    "an arm in a cast for six weeks": dict(more=["hR > .22"]),
    "a bad school report": dict(more=["competence < .55", "ago_move < 1", "stress > .9"], less=["competence > .7"]),
    "a grandparent goes into hospital": dict(req="alive_grandparent > 0", more=["alive_grandparent >= 3"]),
    "the big kids take over the playground": dict(more=["belonging < .5"]),
    "told off in front of the class": dict(more=["hR > .22", "react > 1.1"], less=["hW > .22"]),
    "the cat goes missing": dict(req="had(['a pet of your own', 'a stray dog follows you home'], 6)",
                                 less=["had(['your pet dies'], 2)"]),   # engine: only children who have a pet
    "no holiday this year": dict(more=["money < .13", "harsh > 0"], less=["money > .2"]),
}

# Optional, for the FIRST set (already in earth_rules.INNER_CHILD / READ_CHILD): the same likelier / rarer lines with
# thresholds a child can reach. Only "more" and "less" change; every "req" stays as the engine took it, so the rates the
# first set was calibrated at hold (its req clauses "fails13 >= 1 / 2" are always true and "support > .6" never, as noted).

INNER_CHILD_FIX = {
    "bored on a rainy afternoon": dict(more=["alive_sibling == 0", "autonomy < .6", "hR > .22"], less=["belonging > .75", "hU > .22"]),
    "a friend's new bike stings": dict(more=["money < .12", "alive_sibling >= 1", "hB > .22"],
                                       less=["satisfaction > .65", "had(['someone was kind when it counted'], 1 / 12)", "hG > .22"]),
    "a fib that will not stop nagging": dict(more=["hW + hG > .42", "react > 1.1"], less=["hB > .22", "mk('owned up', 1)"]),
    "everyone laughed when you got it wrong": dict(more=["react > 1.1", "hW > .22", "outlook < .2"], less=["belonging > .75", "steady > .15"]),
    "an empty chair on a special day": dict(more=["ago_death < 3", "belonging < .5"],
                                            less=["held_faith", "belonging > .75", "(ago_death > 5) & (ago_death < 99)"]),
    "a temper that keeps boiling over": dict(more=["health < .5", "hR + hB > .42", "react > 1.1", "mk('made an enemy', 1)"],
                                             less=["steady > .15", "hW + hU > .42"]),
    "the dark at the top of the stairs": dict(more=["age < 8", "react > 1.1", "ago_move < .5"], less=["steady > .15", "age > 9"]),
    "a new baby takes up all the room": dict(more=["belonging < .5", "react > 1.1"], less=["alive_sibling >= 2", "steady > .15"]),
    "nobody watches the cartwheel": dict(more=["hB + hR > .42"], less=["ago_hard_win < 1 / 12", "hG > .22", "steady > .15"]),
    "standing up for someone smaller": dict(more=["hG + hW > .42", "react > 1.1"], less=["stress > 1.2"]),
    "the glow of a gold star": dict(more=["hB + hW > .42"], less=["hG > .22"]),
    "a question that will not go to bed": dict(more=["belonging > .6", "hU > .22", "ago_move < 1"], less=["stress > 1.2", "money < .12"]),
    "an itch to build something": dict(more=["hR + hU > .42", "time > .68"], less=["stress > 1.2"]),
    "too much fizz to sit still": dict(more=["hR + hG > .42"], less=["health < .5", "stress > 1.2"]),
    "someone was kind when it counted": dict(more=["hW + hG > .42", "held_faith"], less=["hB > .22", "stress > 1.2"]),
    "more stars than anyone could count": dict(more=["held_faith", "hG + hU > .42"], less=["time < .66"]),
}
READ_CHILD_FIX = {
    # children's money is about .15, so "money < .2" held for every child: a constant x0.6, not a rarer reading
    "the fair comes to town": dict(more=["prosper > 0"], less=["unrest > 0", "money < .12"]),
    "the school trip": dict(less=["money < .12", "harsh > 0"]),
}
INNER.update(INNER_CHILD_2)
READ.update(READ_CHILD_2)
for k_, v_ in INNER_CHILD_FIX.items():
    INNER[k_].update(v_)
for k_, v_ in READ_CHILD_FIX.items():
    READ[k_].update(v_)

LIFE = {
    # marriage steadies a partnership (yearly separation about 2% married vs 6% or more unmarried); "less" twice = x0.36
    "a breakup": dict(less=["married", "married", "yrs_partner >= 3"]),   # young couples part far more often than settled ones
    # engaged couples marry: about half within a year and most within two (x1.6 four times, so about 6 times as likely)
    "getting married": dict(more=["has('engaged')"] * 4, less=["~has('engaged')"] * 3),   # most weddings follow an engagement
    "a baby on the way, planned or not": dict(more=["held_partner"], less=["~held_partner"]),
    "a child is born": dict(more=["held_partner"], less=["~held_partner"]),
    # Emren's point 12 (2026-10-05): once it has happened it is likelier again (about half of first depressive episodes
    # recur, Burcusa & Iacono 2007; 40 to 60 in 100 relapse after treatment for addiction, NIDA), and a first time is
    # rarer: x0.6 before, x2.6 after (the Library's gap still holds off a repeat for its first years)
    "a long dark season": dict(more=["had(['a long dark season'], 99)"] * 2, less=["~had(['a long dark season'], 99)"]),
    "an addiction takes hold": dict(more=["had(['an addiction takes hold'], 99)"] * 2, less=["~had(['an addiction takes hold'], 99)"]),
    # the Library's gates (drafts/next2/for-the-engine.md): worries end only for someone who had them; a cause wins only
    # for someone who fights for one
    "money worries end": dict(req="(money < .12) | is_poor | had(['money runs out at home', 'losing the home', 'losing your job'], 4)"),
    "a cause you fought for wins": dict(req="held_community | held_faith"),
    "the first months of retirement": dict(req="retired & (ago_retire < 1)"),
    "divorce after twenty years": dict(req="yrs_partner >= 15"),
    "the children leave home": dict(req="yrs_children >= 16"),
    "your first grandchild": dict(req="yrs_children >= 20"),
    "your child's big success": dict(req="yrs_children >= 8"),
    "facing the end": dict(req="(health < .45) | (age >= 80)"),
    # only after a job was lost or left; most find work in the first months, those still looking after a year find it
    # slower (2026-10-05, with FIXES: US men, NLSY79: 22% had a spell of 27 weeks or more by their forties, BLS 2013;
    # displaced workers 2017-19: 70% back in work by January 2020, BLS)
    "your partner falls seriously ill": dict(req="held_partner"),   # Library 14:10 (staged batch)
    # the parents' pair (everyday, needs: children): only while children are at home
    "a vacancy for a parent governor": dict(req="kids_home"),
    "the parents ask you to run the year's events": dict(req="kids_home"),
    "a new job at last": dict(req="~held_career & (ago_end_career < 99) & ~retired", more=["ago_end_career < .5"],
                              less=["ago_end_career >= 1", "ago_end_career >= 2"]),
}

# the batch's own event for finding work again after a lost job (the engine's quiet rejob is off when it is there)
REJOB = "a new job at last"

# adult inner moments and outside events start at 12 (their words are adult); child versions (window ending by 12) keep theirs
INNER_MIN_AGE = 12
READ_MIN_AGE = 12

# fields the engine adds to Library situations (to send back to the Library as fixes)
FIXES = {
    "starting school": dict(once=True),
    # 2026-10-05: per_year .6 read as a yearly rate left 54% still without work after a year and 64% of lives a year
    # or more out of work (catalogue: 15%); with LIFE's more and less: about half back within three months, nine in ten
    # within a year (calib_v7/churn_check.py)
    "a new job at last": dict(per_year=(0.0, 0.0, 4.4, 4.4, 3.6, 1.4)),
    # twice the batch's rate, so that with LIFE's more and less an engaged couple marries at a median of about a year and a
    # half (calib_v7/engaged_check.py) and a couple that is not engaged at under half the batch's rate (game play-test 16:19)
    "getting married": dict(per_year=(0.0, 0.0, 0.14, 0.10, 0.03, 0.0)),
    # Emren's point 12 (2026-10-05): 2.5 births a life at the batch's .08 against about 2.0 (US completed fertility; about
    # 1 in 6 never has a child, CDC): four fifths of the batch's rate
    "a child is born": dict(per_year=(0.0, 0.0, 0.0, 0.064, 0.0004, 0.0)),
    # the Library took in the rest (2026-10-05 06:45): ends on "losing your job", per-eligible rates, moves
}


