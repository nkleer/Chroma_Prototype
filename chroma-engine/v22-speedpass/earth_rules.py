"""Engine-side reading of the Library's modern Earth batch (chroma-library/earth.py, approved by Emren 2026-10-05 05:11).

The Library writes when an inner moment, an echo or an outside event comes in plain words (trigger: requires / likelier /
rarer; after + delay_years; timing). The engine reads those words through the conditions below, written in the engine's
own vocabulary (see COND_VOCAB in batch.py). Parts the engine cannot see (a song on the radio, a friend's promotion this
week) stay in the situation's rate: the condition only says when the moment is possible at all.

Each entry: req (must hold), more (each true clause makes it likelier), less (each true clause makes it rarer).
Echoes also have an anchor: what starts the clock (a mark, a commitment, a stretch of life). The delay window is the
Library's delay_years. Expressions are numpy expressions over one row per person; use & | ~ and parentheses.
"""

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
}

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


# per_year is the population rate; drivers decide who gets an event, not how many there are. DRV_NORM is the mean driver
# multiplier among people an event can happen to (measured on calm lives, seed 21: calib_v7/drv_norm.py; re-measured 2026-10-05 ~17:10 on
# the Library's 16:55 staged batch, 600 lives: drv_norm_staged2.out; within 3% of the 14:50 values; child versions keyed by their own name), and load_batch divides
# per_year by it. Re-measure when the batch's drivers change. Re-measured 2026-10-05 ~23:50 on the Library's next batch (staged
# 23:45, 300 lives: calib_v8/drv_norm_next2.out), which adds 15 life events; most older values moved by under 12%.
DRV_NORM = {
    'a baby on the way, planned or not': 1.092,
    'a best friend of your own': 1.142,
    'a breakthrough in your work': 1.152,
    'a breakup': 0.955,
    'a brother or sister dies': 0.998,
    'a business partner about to ruin you': 1.208,
    'a casting call for children': 0.853,
    'a cause you fought for wins': 1.43,
    'a chair falls vacant at another university': 1.0,
    'a challenge from the back benches': 1.091,
    'a chance to change everything': 1.224,
    'a chance to start a business of your own': 1.062,
    'a child is born': 1.437,
    'a child of your own, another way': 0.967,
    'a close call on the road': 0.905,
    'a close friend moves away': 0.897,
    'a club where you belong': 0.937,
    'a collaboration that goes unusually well': 1.194,
    'a community proposes a better question': 1.521,
    'a crash takes the savings': 1.072,
    'a cure is found at last': 1.027,
    'a deal to get it through': 1.0,
    'a director is needed for the autumn play': 1.265,
    'a discovery nobody asked you for': 1.091,
    'a donor wants a favour': 0.893,
    'a facility looks outside for its next head': 1.0,
    'a fellowship of your own': 1.123,
    'a file on your opponent': 0.978,
    'a finding that makes the news': 1.06,
    'a friend for life': 1.389,
    'a friend who will not wake up': 0.983,
    'a frightening diagnosis': 0.937,
    'a grandparent dies': 0.927,
    'a group of your own, open to all comers': 1.0,
    'a heart attack or stroke': 0.861,
    'a holiday romance': 0.877,
    'a landslide on election night': 1.21,
    'a late love': 1.133,
    'a long dark season': 0.879,
    'a long-lost relative finds you': 1.054,
    'a named fellowship, one a year': 1.076,
    'a narrow escape': 0.853,
    'a national centre opens its posts': 1.0,
    'a new job at last': 1.2,
    'a parent dies': 0.98,
    "a partner's affair comes to light": 0.73,
    'a pet of your own': 0.961,
    'a public scandal': 1.106,
    'a racing heart after a heavy weekend': 0.931,
    'a revival fills the square': 1.097,
    "a rival's result contradicts yours": 1.045,
    'a run for mayor from outside the council': 1.071,
    'a sadness that will not lift': 1.293,
    'a scandal breaks': 1.059,
    "a scientist's post at a famous lab": 1.0,
    'a screen test': 1.0,
    'a search for a new voice for science': 1.092,
    'a seat falls vacant': 1.071,
    'a seat the party cannot win': 1.0,
    'a serious accident or illness': 1.047,
    'a speech that goes everywhere': 1.159,
    'a stranger on the pavement who does not get up': 1.185,
    'a stranger saves you, or you save one': 1.133,
    'a stranger to the rescue': 0.924,
    'a teacher or coach who believes in you': 0.966,
    'a teacher who sees something in you': 0.861,
    'a trip far from home': 0.919,
    'a voice for the cartoon': 1.0,
    'a vote against your conscience': 0.95,
    'an addiction takes hold': 0.908,
    'an error in your published work': 0.951,
    'an invitation for three': 0.831,
    'an offer from people who do not ask twice': 1.36,
    'an old dataset suddenly matters': 1.159,
    'an operation gives something back': 0.947,
    'an operation that makes things better': 0.962,
    'an unexpected chance: a grant, a role, a stage': 1.299,
    'an unexpected legacy': 0.983,
    'betrayed by a friend or a business partner': 0.71,
    'burnout': 1.036,
    'buying a home': 0.977,
    'cast as understudy to the lead': 1.0,
    'casting night at the local players': 1.281,
    'divorce after twenty years': 0.805,
    'earning a qualification': 1.272,
    'election night': 1.0,
    'everyone is suddenly on the new medium': 0.965,
    'facing the end': 1.003,
    'falling in love': 1.067,
    'filmed by chance in the street': 1.258,
    'financial ruin': 1.096,
    'getting married': 1.185,
    'going into foster care': 1.378,
    'growing up with an illness': 0.88,
    "honoured for your life's work": 1.421,
    'leaving acting for another life': 1.06,
    'leaving politics for another life': 1.076,
    'leaving research for another life': 1.148,
    'living with a chronic illness': 0.81,
    'losing a grandparent': 0.925,
    'losing a parent too soon': 1.005,
    'losing the home': 1.02,
    'losing your job': 1.047,
    'making peace with family you had cut off': 1.426,
    'money runs out at home': 1.131,
    'money worries end': 1.0,
    'moving in with a partner': 0.92,
    'moving to a new town': 1.075,
    'moving to a smaller home or into care': 0.722,
    'opening night at the fringe': 1.256,
    'polling day for mayor': 1.0,
    'polling day in the ward': 1.0,
    'pressure to say more than the data show': 1.008,
    'robbed or attacked in the street': 1.021,
    'standing with no party behind you': 1.0,
    'starting school': 1.0,
    'telling the family who you are': 1.012,
    'the badge you worked for': 1.034,
    'the call to serve': 1.0,
    'the campaign loses its organiser': 1.0,
    'the children leave home': 0.952,
    "the city wants the town's show": 1.22,
    'the constituency wants one thing, the party another': 1.071,
    'the contract runs out': 1.1,
    'the cyclist at dusk': 0.971,
    'the director calls again': 1.081,
    'the facility needs a head': 1.123,
    'the family moves to a new town': 1.026,
    'the field season is lost': 1.09,
    'the film you made with friends': 1.116,
    'the first months of retirement': 0.957,
    'the funding call closes on Friday': 0.983,
    'the hustings in the church hall': 1.16,
    'the instrument time you were promised': 1.018,
    'the last week of the painkillers': 1.057,
    'the late starter': 1.07,
    'the lead from the open queue': 1.145,
    'the lead voice in a series': 1.0,
    'the leadership falls vacant': 1.09,
    'the leading player leaves the company': 1.207,
    'the machines come for the work': 1.105,
    'the man who hurt your family walks free': 0.962,
    'the money runs short three weeks out': 1.163,
    'the neighbour who wants your land': 1.072,
    'the night both covers are off': 1.204,
    'the night it goes too far': 1.257,
    'the night you lose the seat': 1.053,
    'the old order falls': 0.903,
    'the old theatre needs someone to save it': 1.35,
    'the other side of the table': 1.0,
    'the part of a lifetime is cast': 1.241,
    'the phone call from the leader': 1.1,
    'the power and the networks go down': 1.061,
    'the reshuffle': 1.09,
    'the script competition': 1.0,
    'the show is a hit': 1.094,
    'the showcase for agents': 1.0,
    'the stage management team is a person short': 1.0,
    'the summer show casts its lead': 1.116,
    'the survey wants a paid assistant': 1.088,
    'the theatre needs an artistic director': 1.0,
    'the town needs a mayor': 1.073,
    'the understudy goes on': 1.297,
    'they want you to lead a group': 1.078,
    'two actors, one part': 1.087,
    'two houses from now on': 1.092,
    'up the ladder to clear the gutters': 1.03,
    'war comes': 0.896,
    'welcomed into a community': 1.437,
    'who stays home with the baby': 1.057,
    'whose name goes first': 0.99,
    'writing in cold for a job in politics': 1.056,
    'you are picked for something special': 0.861,
    'you take in a child who needs a home': 1.235,
    'you win a scholarship or a place': 0.973,
    'your child dies': 1.097,
    'your child falls seriously ill': 1.04,
    "your child's big success": 1.293,
    'your closest friend dies': 1.006,
    'your first full-time job': 1.043,
    'your first grandchild': 1.304,
    'your first real job': 0.914,
    'your parents split up': 1.028,
    'your partner dies': 1.023,
    'your partner falls seriously ill': 1.0,
}








# ---------------------------------------------------------------- titles and perks (chroma-engine/perks-titles-format.md)
# The engine's reading of the Library's plain words (gained, lost, needs) in chroma-library/<world>_perks_titles.py.
# Each entry: req (who can gain it, in the condition vocabulary plus has('name'), was('name'), yrs_has('name')), rate
# (a yearly chance while req holds; left out: the share spread over the age window), after (titles of the same kind it
# grows out of, and replaces), entry (a commitment's first title when the commitment starts; default: no after),
# starts (a background gain also starts its commitment), lose / lrate (a yearly chance of losing it while lose holds),
# weight (practice | colors | money | ties: who is likelier among those who qualify), grants (perks that come with it),
# lwhy (the words for a loss through lose), refines (held on top of another title, as the catalogue's refines: the
# rules set it where the nesting is the engine's reading). A perk with a lose rule is lost only that way (and through
# acts), never slipping away at random. Money gates follow the engine's money among adults 25 to 65 (calib_v7/
# churn_check.py, 2026-10-05): .003 is the poorest tenth, .02 the 15th percentile, .08 the 30th, .2 the median, .25
# the 58th, .45 the 90th.
# Engine-granted, outside these rules: widowed, divorced, retiree, out of work, newcomer, veteran, left the faith.
# Every act field (title:, grants:, takes:, suspends:, requires:) works on top of these, and replaces a background rule
# once the Library has put it on the acts.
SKILLED = "mkn('learned a skill') >= 2"
ROLES = {
    # careers: the first title when a career starts, chosen by fit with the act that started it; a few grow from others
    "shop assistant": dict(), "waiter or bartender": dict(), "care worker": dict(), "factory worker": dict(),
    "office clerk": dict(req="has('school-leaving certificate')"),
    "nurse": dict(req="has('professional registration')"),
    "teacher": dict(req="has('graduate') & has('professional registration')"),
    "electrician": dict(req="has('trade ticket')", after=["apprentice"], rate=0.25, grants=["building trade"]),
    "builder": dict(after=["apprentice"], rate=0.15, entry=True),
    "shop owner": dict(req="has('savings') | has('family business')"),
    "soldier": dict(req="(age <= 30) & ~has('someone with a record')"),
    "farmer": dict(req="has('plot of land') | has('family business')"),
    "software developer": dict(req="has('writing code')"),
    "shift manager": dict(after=["shop assistant", "waiter or bartender", "care worker", "factory worker", "office clerk",
                                 "cook", "delivery driver", "salesperson"], req="(yrs_career >= 1) & has('reliable record')", rate=0.08),
    "police officer": dict(req="(age <= 40) & ~has('someone with a record')"),
    "cook": dict(), "salesperson": dict(), "builder ": None,
    "delivery driver": dict(req="has('driving licence')"),
    "accountant": dict(req="has('bookkeeping')"),
    "estate agent": dict(req="has('driving licence')"),
    "founder of a firm": dict(req="(has('savings') | (money > .6)) & mk('took a wild risk')"),
    "head chef": dict(after=["cook"], req="yrs_career >= 4", rate=0.08),
    "apprentice": dict(req="age <= 30"),
    # partners: a first love, then moving in, engagement, marriage, many years
    "girlfriend or boyfriend": dict(),
    "living together": dict(after=["girlfriend or boyfriend"], req="(yrs_partner >= 1) & (age >= 18)", rate=0.35),
    "engaged": dict(after=["girlfriend or boyfriend", "living together"], req="(yrs_partner >= 1.5) & (age >= 19)", rate=0.12,
                    # game play-test 16:19 (engaged for 17 years): most engaged couples marry within two years (LIFE: getting
                    # married is much likelier while engaged); one still engaged after three years mostly breaks it off
                    lose=[("yrs_has('engaged') >= 3", "the engagement broken off")], lrate=0.35, lend="broke up"),
    "married again": dict(after=["girlfriend or boyfriend", "living together", "engaged"], req="married & (was('divorced') | was('widowed'))", rate=1.0),
    "wife or husband": dict(after=["girlfriend or boyfriend", "living together", "engaged"], req="married & ~was('divorced') & ~was('widowed')", rate=1.0),
    "partner of many years": dict(after=["wife or husband", "living together", "married again"], req="yrs_partner >= 20", rate=0.5),
    # children
    # a parent stays one: three or more, single parent and grandparent are held on top of mother or father (2026-10-05:
    # as successions they took it away and gave it back, and its facets with it)
    "mother or father": dict(entry=True),
    "parent of three or more": dict(refines="mother or father", req="has('mother or father') & (yrs_children >= 3) & (yrs_children <= 15) & held_partner", rate=0.03),
    "single parent": dict(refines="mother or father", req="has('mother or father') & kids_home & ~held_partner & (ago_end_partner >= 1)", rate=0.5,
                          lose="(held_partner & (yrs_partner >= 1)) | ~kids_home", lrate=1.0, lwhy="a partner at home, or the children grown"),
    "stepparent": dict(req="held_partner & (yrs_partner < 3) & ~held_children & (age >= 22)", rate=0.04, starts=True, entry=False),
    "foster parent": dict(req="(age >= 25) & (money > .4) & mk('helped someone in need')", rate=0.0015, starts=True),
    "adoptive parent": dict(req="(age >= 25) & held_partner & ~held_children & (yrs_partner >= 3)", rate=0.003, starts=True),
    "grandparent": dict(refines="mother or father", req="has('mother or father') & (yrs_children >= 22)", rate=0.12),
    # community: up to three at once; children's teams and troops start the commitment on their own
    "on the team": dict(req="(age <= 40) & ((hR + hG + hB) > .55)", rate=0.06, starts=True, weight="colors"),
    "scout or guide": dict(req="age <= 14", rate=0.03, starts=True),
    "prefect": dict(req="has('teachers\\' favourite') & (age >= 13)", rate=0.1, starts=True),
    "team captain": dict(after=["on the team"], req="yrs_has('on the team') >= 2", rate=0.08),
    "neighbourhood volunteer": dict(req="mk('helped someone in need')", rate=0.02, starts=True, weight="colors"),
    "union rep": dict(req="held_career & (yrs_career >= 3) & mk('defied an authority')", rate=0.02),
    "local councillor": dict(req="has('good name in town') & (age >= 25)", rate=0.004),
    "youth coach": dict(req="was('on the team') & (age >= 25) & held_children", rate=0.02),
    "residents' committee member": dict(req="has('homeowner')", rate=0.004),
    "club treasurer": dict(req="has('bookkeeping') & has('reliable record')", rate=0.01),
    "in a street gang": dict(req="(age <= 25) & ((money < .3) | mk('made an enemy'))", rate=0.004, starts=True, lose="age > 25", lrate=0.3),
    # faith, ideology or cause
    "regular worshipper": dict(),
    "deacon or elder": dict(after=["regular worshipper"], req="(yrs_faith >= 10) & has('known face at worship')", rate=0.01),
    "activist in a cause": dict(req="had(['a sense of injustice', 'a protest in your city'], 2)", rate=0.04, weight="colors", starts=True),
    "party member": dict(req="age >= 18", rate=0.004, weight="colors", starts=True, entry=True), "convert": dict(req="~was('regular worshipper') | was('left the faith')"),
    "seeker": dict(),
    # statuses
    "graduate": dict(req="has('school-leaving certificate') & (age >= 20) & (age <= 30)", rate=0.08, weight="colors"),
    "veteran": None, "widowed": None, "retiree": None, "newcomer": None, "divorced": None, "out of work": None,
    "has killed in war": dict(req="has('soldier') & (yrs_career >= 1)", rate=0.05),   # most who serve never do
    "homeowner": dict(req="(age >= 22) & ((money > .5) | has('savings') | has('inheritance'))", rate=0.12),
    "immigrant": dict(req="ago_move < 1", rate=0.2),
    "someone with a record": dict(req="mk('defied an authority', 1) | mk('hid a wrong', 1) | mk('took a wild risk', 1)", rate=0.03),
    "ex-prisoner": dict(req="has('someone with a record') & mk('defied an authority', 2)", rate=0.02),
    "in recovery": dict(req="had(['an addiction takes hold'], 5)", rate=0.25),
    "eldest child": dict(req="(age <= 6) & (older_siblings == 0) & (younger_siblings > 0)", rate=0.6),   # N4: first-born with a younger one
    # (rate .6 a year: most first-borns take it within a year or two of the first younger one; .12 reached .13 of lives
    # against a share of .35, Library next3 §1)
    "carer for a parent": dict(req="(alive_parent > 0) & (age >= 30)", rate=0.012),
    "homeless": dict(req="(money < .08) & (ties < .3)", rate=0.1),
    "cancer survivor": dict(req="had(['a frightening diagnosis'], 1) & (health > .4)", rate=0.4),
    "left the faith": None,
    # perks: skills come with practice in their ways (weight practice); credentials and assets with their prerequisites
    "swimming": dict(req="age <= 14", rate=0.12),
    "cooking for a crowd": dict(req="had(['learning to cook for yourself', 'a holiday meal with the whole family'], 3)", rate=0.05),
    "second language": dict(rate=0.02), "musical instrument": dict(req="has('instrument of one\\'s own')", rate=0.08),
    "building trade": dict(req="has('apprentice') | has('builder')", rate=0.3),
    "fixing things": dict(req="mk('learned a skill')", rate=0.025), "car mechanics": dict(req=SKILLED, rate=0.006),
    "growing food": dict(req="had(['tending an allotment'], 3) | (age <= 14)", rate=0.025),
    "sewing and mending": dict(req="mk('learned a skill')", rate=0.012),
    "public speaking": dict(req="mk('learned a skill') & mk('took a wild risk')", rate=0.012),
    "bookkeeping": dict(req="mk('learned a skill') & (age >= 16)", rate=0.015),
    "boxing or martial arts": dict(req=SKILLED + " & (age <= 40)", rate=0.005),
    "dancing": dict(rate=0.008), "writing code": dict(req=SKILLED, rate=0.005),
    "drawing and painting": dict(req="mk('learned a skill')", rate=0.006),
    "home nursing": dict(req="mkn('helped someone in need') >= 2 | has('carer for a parent')", rate=0.012),
    "hunting and fishing": dict(rate=0.004), "selling": dict(req="mk('made a friend') | mk('took a wild risk')", rate=0.008),
    "finding things out": dict(req="mk('learned a skill')", rate=0.012),
    "minding small children": dict(req="mk('helped someone in need') | held_children", rate=0.03),
    "calming people down": dict(req="mkn('helped someone in need') >= 2", rate=0.008),
    "striking a deal": dict(req="mk('took a wild risk') & (age >= 16)", rate=0.008), "scripture": dict(req="was('regular worshipper')", rate=0.05),
    "cards for money": dict(req="mk('took a wild risk')", rate=0.004), "teaching": dict(req="mk('learned a skill') & mk('helped someone in need')", rate=0.008),
    "driving licence": dict(req="(age >= 17) & ((age < 30) | chance(.15))", rate=0.1),   # most learn young (2026-10-05)
    "first-aid certificate": dict(rate=0.01), "passport": dict(rate=0.06),
    "school-leaving certificate": dict(req="(age >= 16) & (age <= 20)", rate=0.6, weight="practice"),
    "professional registration": dict(req="has('graduate') & (age <= 40)", rate=0.07, weight="practice"),   # 10-09 floors (Emren: rare titles reachable): about 3 graduates in 10
    # within 5 years, likelier for those who practise its ways (the road to physician, veterinarian, pharmacist)
    "lorry or bus licence": dict(req="has('driving licence') & held_career", rate=0.002),
    "trade ticket": dict(req="(has('apprentice') & (yrs_career >= 2)) | (has('building trade') & (age >= 20))", rate=0.15),
    "hunting licence": dict(req="has('hunting and fishing') & ~has('someone with a record')", rate=0.15),
    "motorbike licence": dict(rate=0.004), "citizenship": dict(req="has('immigrant')", rate=0.04),
    "drinks licence": dict(req="~has('someone with a record') & held_career", rate=0.001),
    "coaching badge": dict(req="was('on the team') & (age >= 18)", rate=0.004),
    "referee's badge": dict(req="was('on the team')", rate=0.002),
    "good name in town": dict(req="(mkn('kept your word') >= 3) & (mkn('helped someone in need') >= 3) & (ago_move > 3)", rate=0.04,
                              lose="mk('hid a wrong', 1) | (ago_move < 1)", lrate=0.5),
    "rank": dict(req="(yrs_career >= 5) & has('reliable record')", rate=0.025, lose="~held_career", lrate=1.0),
    "known face at worship": dict(req="has('regular worshipper') & (yrs_faith >= 3)", rate=0.1, lose="~held_faith | (ago_move < 1)", lrate=1.0),
    "reliable record": dict(req="mkn('kept your word') >= 3", rate=0.08, lose="mk('broke your word', 1)", lrate=0.4),
    "good credit": dict(req="(age >= 18) & (money >= .08)", rate=0.15, lrate=0.5,
                        lose=[("had(['financial ruin'], 1)", "financial ruin"), ("(money < .01) & (yrs_adj('poor') >= 1)", "missed payments")]),
    "the one everyone asks": dict(req="(age >= 25) & (mkn('learned a skill') >= 5)", rate=0.01),
    "following online": dict(req="had(['wanting to be noticed'], 2)", rate=0.04),
    "name in the field": dict(req="(yrs_career >= 10) & (mkn('learned a skill') >= 8)", rate=0.006),
    "not to be crossed": dict(req="mkn('made an enemy') >= 3", rate=0.01),
    "regular at the local": dict(req="(age >= 18) & mk('made a friend')", rate=0.015, lose="ago_move < 1", lrate=1.0),
    "local hero": dict(req="mk('helped someone in need', 1) & mk('took a wild risk', 1)", rate=0.01),
    "old family name": dict(req="age <= 4", rate=0.02, lose="ago_move < 1", lrate=0.5),
    "inner circle at work": dict(req="held_career & (yrs_career >= 5)", rate=0.008, lose="~held_career", lrate=1.0),
    "teachers' favourite": dict(req="age <= 16", rate=0.04, weight="practice"),
    "mentor": dict(req="mk('learned a skill') | mk('helped someone in need')", rate=0.03),
    "friend in power": dict(req="mkn('made a friend') >= 3", rate=0.003),
    "patron": dict(req="mk('took a wild risk') & (mkn('learned a skill') >= 4)", rate=0.002),
    "family who will always take you in": dict(req="age <= 4", rate=0.5),
    "friend for life": dict(req="mk('made a friend')", rate=0.03, lose="alive_friend < 1", lrate=1.0),
    "old school network": dict(req="has('graduate')", rate=0.08),
    "sponsor in recovery": dict(req="has('in recovery')", rate=0.5),
    "neighbour who has your back": dict(req="(age >= 18) & (mk('made a friend') | mk('helped someone in need'))", rate=0.03, lose="ago_move < 1", lrate=1.0),
    "contact in the trade": dict(req="held_career & (yrs_career >= 3)", rate=0.015),
    "family abroad": dict(req="(age <= 4) | has('immigrant')", rate=0.06),
    "old comrades": dict(req="(was('soldier') & (yrs_career >= 3)) | (yrs_has('on the team') >= 5)", rate=0.05),
    "godparent who looks out": dict(req="age <= 4", rate=0.15, lose="age >= 60", lrate=1.0),
    "dog of one's own": dict(req="had(['a pet of your own', 'a stray dog follows you home'], 1)", rate=0.5, lose="had(['your pet dies'], 1)", lrate=1.0),
    "in-laws who took you in": dict(req="has('wife or husband') | has('living together') | has('married again')", rate=0.15,
                                    lose="~held_partner", lrate=0.7),
    "savings": dict(req="(age >= 14) & (money >= .25)", rate=0.2, lrate=0.5,
                    lose=[("had(['financial ruin'], 1)", "financial ruin"), ("had(['losing your job'], 1) & (money < .1)", "spent while out of work"),
                          ("(money < .03) & (yrs_adj('poor') >= 1)", "spent in hard times")]),
    "paid-off home": dict(req="has('homeowner') & (yrs_has('homeowner') >= 20)", rate=0.1),
    "car": dict(req="has('driving licence') & (money > .02)", rate=0.3, lrate=0.5,
                lose=[("had(['financial ruin'], 1)", "financial ruin"), ("(money < .003) & (yrs_adj('poor') >= 2) & chance(.3)", "no money to keep it"),
                      ("(age >= 75) & (health < .35)", "the doctor says to stop driving")]),
    "family business": dict(req="age < 15", rate=0.07),          # a family business one can join at fourteen
    "inheritance": dict(req="ago_death < 1", rate=0.3),
    "workplace pension": dict(req="held_career & (yrs_career >= 2) & (age >= 22)", rate=0.12),
    "plot of land": dict(req="had(['tending an allotment'], 3) | has('farmer')", rate=0.05),
    "shares": dict(req="(has('savings') | has('workplace pension')) & (money > .45)", rate=0.04),
    "van and tools": dict(req="(has('trade ticket') | has('building trade')) & has('driving licence')", rate=0.1),
    "flat to rent out": dict(req="(has('savings') | has('inheritance')) & has('good credit') & (money > .55)", rate=0.01),
    "place by the sea": dict(req="(has('savings') | has('inheritance')) & (money > .55) & (age >= 40)", rate=0.006),
    "scholarship": dict(req="(age >= 11) & (age <= 20) & (mkn('learned a skill') >= 3)", rate=0.02),
    "workshop": dict(req="has('fixing things')", rate=0.02),
    "instrument of one's own": dict(req="age <= 30", rate=0.012),
}
# ---- volume 2: Emren's 100 more titles (12:05), the Library's rules proposal (chroma-library/drafts/titles2/roles-v2.py,
# taken in 2026-10-05 ~14:30; engine changes marked "engine"). A catalogue without these titles (the first draft)
# runs as before: their names are in ROLES_OPTIONAL.
ROLES_V2 = {
    # ---------------- careers (T2-001 to T2-045)
    # health and emergency services
    "laboratory technician": dict(req="has('school-leaving certificate')"),
    "paramedic": dict(req="has('professional registration') & has('driving licence') & (health > .5)",
                      lose="health < .4", lrate=0.3),
    "physician": dict(req="has('graduate') & has('professional registration') & (age >= 24)",
                      lose="~has('professional registration') & (age < 70)", lrate=1.0),
    "psychotherapist": dict(req="has('graduate') & (age >= 25)", after=["nurse", "teacher"], rate=0.003, entry=True),
    "pharmacist": dict(req="has('graduate') & has('professional registration')"),
    "veterinarian": dict(req="has('graduate') & has('professional registration')"),
    "midwife": dict(req="has('professional registration')", after=["nurse"], rate=0.01, entry=True,
                    lose="~has('professional registration') & (age < 70)", lrate=1.0),
    "firefighter": dict(req="(age >= 18) & (age <= 40) & ~has('someone with a record') & (health > .6)",
                        lose="health < .45", lrate=0.3),
    "emergency dispatcher": dict(req="(age >= 18) & ~has('someone with a record')",
                                 after=["paramedic", "firefighter", "police officer"], rate=0.01, entry=True),
    # words, records and heritage
    "translator": dict(req="has('second language') & (age >= 20)"),
    "journalist": dict(req="has('graduate') | has('finding things out')"),
    "book editor": dict(req="has('graduate')", after=["journalist"], rate=0.005, entry=True),
    "archivist": dict(req="has('graduate')"),
    "museum curator": dict(req="has('graduate')", after=["archivist", "archaeologist"], rate=0.02, entry=True),
    "archaeologist": dict(req="has('graduate')"),
    # land, buildings and systems
    "land surveyor": dict(req="(has('graduate') | was('apprentice')) & (age >= 18)"),
    "urban planner": dict(req="has('graduate')"),
    "architect": dict(req="has('graduate') & has('professional registration')"),
    "civil engineer": dict(req="has('graduate')"),
    "data analyst": dict(req="has('graduate') | has('writing code') | has('finding things out')",
                         after=["office clerk", "accountant"], rate=0.01, entry=True),
    "cybersecurity analyst": dict(req="has('writing code')", after=["software developer", "data analyst"], rate=0.02,
                                  entry=True),
    # trades and making
    "machinist": dict(req="was('apprentice') | (mkn('learned a skill') >= 2)", after=["apprentice", "factory worker"],
                      rate=0.05, entry=True),
    "welder": dict(req="was('apprentice') | has('building trade') | (mkn('learned a skill') >= 2)",
                   after=["apprentice", "factory worker", "builder"], rate=0.04, entry=True),
    "plumber": dict(req="has('trade ticket') | has('building trade')", after=["apprentice", "builder"], rate=0.1,
                    entry=True),
    "carpenter": dict(req="has('building trade') | has('trade ticket')", after=["apprentice", "builder"], rate=0.1,
                      entry=True),
    "baker": dict(req="age >= 16", after=["cook", "shop assistant"], rate=0.01, entry=True),
    # services that keep a place running
    "cleaner": dict(),
    "sanitation worker": dict(req="age >= 18"),
    "postal worker": dict(req="age >= 17"),
    "train driver": dict(req="(age >= 20) & (age <= 50) & ~has('someone with a record') & (health > .6)",
                         lose="(health < .45) | has('someone with a record')", lrate=0.5),
    "commercial pilot": dict(req="(age >= 19) & (age <= 45) & ~has('someone with a record') & (health > .6) & "   # 10-09 floors (Emren: rare titles reachable): to 45
                                 "(has('savings') | has('graduate') | was('soldier'))",
                             after=["soldier"], rate=0.003, entry=True, lose="health < .5", lrate=0.5),
    # sea, land and living things
    "merchant seafarer": dict(req="(age >= 16) & (age <= 45) & (health > .6)"),
    "commercial fisher": dict(req="(age >= 16) & (health > .5) & (has('family business') | (age <= 35))"),
    "forester": dict(req="has('graduate') | was('apprentice')"),
    "professional beekeeper": dict(req="(age >= 20) & ((mkn('learned a skill') >= 2) | has('beekeeping'))", after=["farmer"],
                                   rate=0.015,   # 10-09 floors (Emren: rare titles reachable): 2 skills or beekeeping, .003 to .015
                                   entry=True),
    # ceremonies, craft and performance
    "funeral director": dict(req="(age >= 20) & (has('family business') | (mkn('helped someone in need') >= 2) | "
                                 "was('care worker'))"),   # 10-09 floors (Emren: rare titles reachable): a care worker's road
    "civil celebrant": dict(req="(age >= 25) & has('public speaking')"),
    "tattoo artist": dict(req="(age >= 18) & has('drawing and painting')"),
    "sound engineer": dict(req="has('musical instrument') | (mkn('learned a skill') >= 2)"),
    "stage technician": dict(req="(age >= 17) & (has('fixing things') | (mkn('learned a skill') >= 2))"),
    "video-game developer": dict(req="has('writing code') | has('drawing and painting')", after=["software developer"],
                                 rate=0.01, entry=True),
    "professional athlete": dict(req="(age >= 16) & (age <= 30) & was('on the team') & (health > .7)",
                                 lose="health < .55", lrate=0.3),
    "novelist": dict(req="(age >= 20) & (mkn('learned a skill') >= 3)", after=["journalist", "book editor", "teacher"],
                     rate=0.002, entry=True),
    "court interpreter": dict(req="has('second language') & ~has('someone with a record') & (age >= 23)",
                              after=["translator"], rate=0.03, entry=True, lose="has('someone with a record')",
                              lrate=1.0),
    "professional conservator": dict(req="has('graduate')"),

    # ---------------- partner, children, community, faith and status (T2-046 to T2-100)
    # partners: four facets on wife or husband, one partnership of its own that starts the commitment
    "newlywed": dict(req="(has('wife or husband') & (yrs_has('wife or husband') < 1)) | (has('married again') & (yrs_has('married again') < 1))", rate=1.0, entry=False),   # Library 15:50
    # granted by an act (title: on a moment about a partner falling ill); the engine does not model a partner's health.
    # No rate, so it is no background rule: the lasts cap (10) and the refined title's end close it
    "caregiving partner": dict(req="held_partner", entry=False, lose="~held_partner", lrate=1.0),   # Library 15:50: any partner
    "nonromantic life partner": dict(req="(age >= 20) & ~held_partner & (mkn('made a friend') >= 2)", rate=0.0005,
                                     starts=True, entry=False, weight="ties"),
    "spouse in a family-arranged marriage": dict(req="has('wife or husband') & (yrs_has('wife or husband') < 1)",
                                                 rate=0.03, entry=False, weight="ties"),
    "partner in a multigenerational household": dict(req="has('wife or husband') & (alive_parent > 0) & (ago_move >= 1)",
                                                     rate=0.004, entry=False, weight="ties",
                                                     lose="(alive_parent < 1) | (ago_move < 1)", lrate=0.5),
    # children: six facets on mother or father, one on grandparent, and a guardianship that starts the commitment
    "parent of an only child": dict(req="has('mother or father') & (yrs_children >= 4) & ~was('parent of an only child') & "
                                        "~had(['a child is born', 'a baby on the way, planned or not'], 4)",   # engine: once
                                    rate=0.1, entry=False, lose="had(['a child is born'], 1)", lrate=1.0),
    "parent of independent adult children": dict(req="has('mother or father') & held_children & ~kids_home", rate=0.5,
                                                 entry=False),
    "parent with a child living abroad": dict(req="has('mother or father') & (yrs_children >= 18)", rate=0.004,
                                              entry=False, lose="yrs_has('parent with a child living abroad') >= 2",
                                              lrate=0.1),
    "home-educating parent": dict(req="has('mother or father') & kids_home & (yrs_children >= 4) & (yrs_children <= 16)",
                                  rate=0.003, entry=False, lose="yrs_has('home-educating parent') >= 1", lrate=0.2),
    "guardian of an unrelated child": dict(req="(age >= 21) & mk('helped someone in need')", rate=0.0003, starts=True,
                                           lose="yrs_has('guardian of an unrelated child') >= 5", lrate=0.2),
    "grandparent raising a grandchild": dict(req="has('grandparent') & (age <= 75)", rate=0.001, entry=False,
                                             lose="yrs_has('grandparent raising a grandchild') >= 3", lrate=0.1),
    "parent coordinating complex support needs": dict(req="has('mother or father') & kids_home & (yrs_children >= 1)",
                                                      rate=0.003, entry=False, lose="~kids_home", lrate=0.3),
    "parent raising a child across languages": dict(req="has('mother or father') & kids_home & "
                                                        "(has('second language') | has('immigrant') | has('family abroad'))",
                                                    rate=0.05, entry=False, lose="~kids_home", lrate=0.5),
    # community: each can start the community commitment (up to three titles at once) and is a possible first title
    "choir member": dict(req="age >= 8", rate=0.004, starts=True, weight="colors"),
    "community-garden coordinator": dict(req="(age >= 18) & (had(['tending an allotment'], 3) | has('growing food'))",
                                         rate=0.004, starts=True, weight="colors"),
    "repair-cafe volunteer": dict(req="(age >= 16) & (has('fixing things') | has('sewing and mending') | has('car mechanics'))",
                                  rate=0.003, starts=True, weight="colors"),
    "amateur astronomer in a club": dict(req="(age >= 10) & (had(['more stars than anyone could count', "
                                             "'the sun goes dark at noon', 'awe'], 10) | has('finding things out'))",
                                         rate=0.002, starts=True, weight="colors"),
    "historical reenactment member": dict(req="age >= 14", rate=0.0003, starts=True, weight="colors"),
    "community-radio presenter": dict(req="(age >= 16) & (has('public speaking') | mk('learned a skill'))", rate=0.0003,
                                      starts=True, weight="colors"),
    "community-mediation volunteer": dict(req="(age >= 21) & has('calming people down')", rate=0.002, starts=True,
                                          weight="colors"),
    "search-and-rescue volunteer": dict(req="(age >= 18) & (age <= 60) & (has('first-aid certificate') | has('keeping fit')) & "
                                            "(health > .6)", rate=0.01,   # 10-09 floors (Emren: rare titles reachable): or keeping fit, .002 to .01
                                        starts=True, lose="health < .4", lrate=0.5),
    "lifeboat volunteer": dict(req="(age >= 17) & (age <= 55) & has('swimming') & (health > .6)", rate=0.0002,
                               starts=True, lose="health < .4", lrate=0.5),
    "school-governance board member": dict(req="(age >= 21) & (kids_home | has('good name in town'))", rate=0.002,
                                           starts=True, lose="yrs_has('school-governance board member') >= 4", lrate=0.4),
    "parent-association organiser": dict(req="kids_home & (yrs_children >= 4) & (yrs_children <= 16)", rate=0.005,
                                         starts=True, lose="~kids_home | (yrs_has('parent-association organiser') >= 3)",
                                         lrate=0.4),
    "housing-cooperative member": dict(req="(age >= 18) & (ago_move >= 1)", rate=0.002, starts=True,
                                       lose="ago_move < 1", lrate=1.0),
    "sports referee": dict(req="has('referee\\'s badge')", rate=0.3, starts=True, lose="~has('referee\\'s badge')",
                           lrate=0.5),
    "festival organiser": dict(req="(age >= 16) & (mkn('made a friend') >= 2)", rate=0.0005, starts=True,
                               weight="colors", lose="had(['burnout'], 1)", lrate=0.5),
    "amateur band member": dict(req="(age >= 12) & has('musical instrument')", rate=0.05, starts=True, weight="colors"),
    "book-club organiser": dict(req="(age >= 16) & mk('made a friend')", rate=0.001, starts=True, weight="colors"),
    "community-kitchen volunteer": dict(req="(age >= 16) & mk('helped someone in need')", rate=0.002, starts=True,
                                        weight="colors"),
    "neighbourhood-watch coordinator": dict(req="(age >= 21) & (ago_move >= 1) & "
                                                "had(['break-ins on the street', 'robbed or attacked in the street'], 2)",
                                            rate=0.05, starts=True, lose="ago_move < 1", lrate=1.0),
    "prison visitor": dict(req="(age >= 21) & (mkn('helped someone in need') >= 2)", rate=0.0002, starts=True,
                           weight="colors"),
    "board-game club organiser": dict(req="(age >= 14) & mk('made a friend')", rate=0.0007, starts=True, weight="colors"),
    # faith and causes: religious roles grow from a faith already held (and replace its title); causes start the faith
    # commitment like [activist in a cause]
    "ordained religious minister": dict(after=["regular worshipper", "deacon or elder", "convert"],
                                        req="(yrs_faith >= 3) & (age >= 23) & has('scripture')", rate=0.002),
    "member of a monastic community": dict(after=["regular worshipper", "convert", "seeker"],
                                           req="(age >= 18) & ~held_partner & ~kids_home", rate=0.0005),
    "lay religious teacher": dict(after=["regular worshipper", "convert"],
                                  req="(yrs_faith >= 3) & (age >= 16) & (has('scripture') | has('teaching') | (yrs_faith >= 8))",
                                  rate=0.01),   # Library 13:55: no test life met scripture or teaching, so long practice counts too
    "congregation musician": dict(after=["regular worshipper", "believer on the big days", "convert"],
                                  req="(age >= 12) & has('musical instrument')", rate=0.02),
    "interfaith-dialogue participant": dict(after=["regular worshipper", "deacon or elder", "convert", "seeker"],
                                            req="(age >= 16) & (yrs_faith >= 2) & mk('made a friend')", rate=0.003),
    "animal-shelter campaigner": dict(req="(age >= 14) & (had(['a pet of your own', 'a stray dog follows you home', "
                                          "'your pet dies'], 10) | has('dog of one\\'s own'))",
                                      rate=0.003, starts=True, weight="colors"),
    "disability-rights organiser": dict(req="(age >= 16) & (had(['living with a chronic illness', "
                                            "'a serious accident or illness', 'a sense of injustice'], 3) | "
                                            "has('parent coordinating complex support needs') | has('carer for a parent'))",
                                        rate=0.01, starts=True, weight="colors"),   # 10-09 floors (Emren: rare titles reachable): .002 to .01
    "civil-liberties campaigner": dict(req="(age >= 16) & had(['a sense of injustice', 'a protest in your city', "
                                           "'a bitter election'], 2)", rate=0.003, starts=True, weight="colors"),
    "restorative-justice advocate": dict(req="(age >= 18) & (had(['a sense of injustice', "
                                             "'robbed or attacked in the street'], 3) | was('someone with a record'))",
                                         rate=0.002, starts=True, weight="colors"),
    "digital-rights advocate": dict(req="(age >= 16) & (has('writing code') | has('finding things out') | "
                                        "had(['someone starts mocking you online'], 3))",
                                    rate=0.002, starts=True, weight="colors"),
    # statuses: no colors; facts of a history (lasts life) or spells that end when what they need stops holding
    "doctoral graduate": dict(req="has('graduate') & (age >= 25) & (age <= 45) & (mkn('learned a skill') >= 3)",
                              rate=0.002),
    "first-generation university student": dict(req="has('school-leaving certificate') & (age >= 17) & (age <= 25) & "
                                                    "~has('graduate') & ~was('first-generation university student')",
                                                rate=0.05, lose="has('graduate')", lrate=1.0),
    "former foster child": dict(req="False"),   # Library 16:55: only through the child event 'going into foster care'
    "adopted person": dict(req="age < 3.05", rate=0.02),   # Library 16:55: a fact of the family story from the start (the
                                                           # engine's lives begin at 3, so: their first month)
    # a claim granted: the applicant becomes a refugee (after), settled as an immigrant (grants); citizenship ends the
    # refugee status, and naturalised citizen comes with it
    "refugee": dict(after=["asylum applicant"], req="yrs_has('asylum applicant') >= .5", rate=0.6, grants=["immigrant"],
                    lose="has('citizenship')", lrate=1.0),
    "asylum applicant": dict(req="(ago_move < 1) & (had(['war comes'], 3) | mk('moved away', 1)) & "
                                 "~was('asylum applicant')", rate=0.01,
                             lose="yrs_has('asylum applicant') >= 1", lrate=0.3),
    "naturalised citizen": dict(req="has('citizenship') & has('immigrant')", rate=1.0),   # gained with [citizenship]
    "bankruptcy or insolvency in their history": dict(req="had(['financial ruin'], 2)", rate=0.5),
    "on probation or community supervision": dict(req="(has('someone with a record') & "
                                                      "(yrs_has('someone with a record') < 1)) | "
                                                      "(has('ex-prisoner') & (yrs_has('ex-prisoner') < 1))",
                                                  rate=0.4, lose="yrs_has('on probation or community supervision') >= 1",
                                                  lrate=0.5),
    "living in residential care": dict(req="(had(['moving to a smaller home or into care'], 1) & (age >= 60)) | "
                                           "((age >= 80) & (health < .5))", rate=0.1, lose="health > .6", lrate=0.2),   # Library 13:55: health < .3 at 75 was
                                           # too rare in test lives (2 in 100 against the share's 15)
    "returned migrant": dict(req="(age >= 20) & mk('came home', 1) & (mkn('moved away') >= 1)", rate=0.3),
    "displaced by a disaster": dict(req="had(['losing the home', 'war comes'], 1)", rate=0.15,
                                    lose="~had(['losing the home', 'war comes'], 1)", lrate=0.5),
}
# ---- perks volume 2 (Emren 15:46; the Library's drafts/perks2/roles-perks2.py of 16:40, as written): ROLES_P2, 85 perk
# rules, and TITLE_LINKS, an overlay on 34 title rules (req, lose and lrate replace the title's own; grants add; why is a
# comment). Like volume 2's titles, a catalogue without these perks still loads (ROLES_OPTIONAL).
ROLES_P2 = {
    # ---------------- p1_access
    # ---------------- credentials
    # transport: the job's licence, its medical and its record
    "airline pilot licence": dict(req="has('commercial pilot') & (health >= .5) & ~has('someone with a record')",
                                  rate=1.0, lrate=0.5,
                                  lose=[("health < .5", "failed the medical"),
                                        ("has('someone with a record')", "a conviction"),
                                        ("~has('commercial pilot')", "let it lapse after leaving the airline")]),
    "train driving licence": dict(req="has('train driver') & (health >= .45) & ~has('someone with a record')",
                                  rate=1.0, lrate=0.5,
                                  lose=[("health < .45", "failed the medical"),
                                        ("has('someone with a record')", "a conviction"),
                                        ("~has('train driver')", "lapsed after leaving the cab")]),
    # the sea: the seafarer's own papers, and the survival course every boat asks for
    "seafarer's papers": dict(req="(has('merchant seafarer') | ((age >= 18) & (age <= 35) & has('swimming') & "
                                  "had(['a trip far from home', 'the itch to be somewhere else'], 2))) & (health >= .45)",
                              rate=0.0029, lrate=0.3,
                              lose=[("health < .45", "failed the seafarer medical"),
                                    ("~has('merchant seafarer') & (yrs_has('seafarer\\'s papers') >= 2)",
                                     "let them lapse ashore")]),
    "sea survival certificate": dict(req="has('commercial fisher') | has('lifeboat volunteer') | has('merchant seafarer') | "
                                         "((has('welder') | has('rigging ticket') | has('trade ticket')) & (age <= 55))",
                                     rate=0.0038, lrate=0.5,
                                     lose="~has('commercial fisher') & ~has('lifeboat volunteer') & "
                                          "~has('merchant seafarer') & (yrs_has('sea survival certificate') >= 4)",
                                     lwhy="lapsed without a refresher"),
    "fishing licence": dict(req="has('hunting and fishing') | has('commercial fisher') | "
                                "((age >= 12) & had(['a day at the beach', 'a weekend hike'], 1))", rate=0.011),
    # trades: tickets that come after the apprenticeship, and lapse when the trade is left
    "gas safety registration": dict(req="(has('plumber') & (yrs_career >= 2)) | (has('trade ticket') & (age >= 21) & chance(.1))",
                                    rate=0.032, lose="~has('plumber') & ~has('trade ticket')", lrate=0.5,
                                    lwhy="lapsed after leaving the trade"),
    "welding certificate": dict(req="has('welder') | ((has('apprentice') | has('machinist') | has('builder')) & "
                                    "(mkn('learned a skill') >= 2))",
                                rate=0.002, lose="~has('welder') & ~has('machinist') & ~has('builder')", lrate=0.3,
                                lwhy="lapsed out of use"),
    "site safety card": dict(req="(age >= 16) & (has('builder') | has('carpenter') | has('welder') | has('plumber') | "
                                 "has('electrician') | has('civil engineer') | has('land surveyor') | "
                                 "(has('apprentice') & has('building trade')))",
                             rate=0.22, lrate=0.5,
                             lose="~has('builder') & ~has('carpenter') & ~has('welder') & ~has('plumber') & "
                                  "~has('electrician') & ~has('civil engineer') & ~has('land surveyor') & "
                                  "~has('apprentice') & (yrs_has('site safety card') >= 5)",
                             lwhy="ran out after years off the sites"),
    "rigging ticket": dict(req="(has('stage technician') & (yrs_career >= 1)) | "
                               "((has('builder') | has('welder')) & (yrs_career >= 2) & chance(.2))", rate=0.043),
    "chainsaw ticket": dict(req="(age >= 16) & (has('forester') | has('farmer') | "
                                "((has('plot of land') | has('hunting and fishing') | has('fixing things')) & chance(.1)))",
                            rate=0.018),
    "chartered status": dict(req="(has('civil engineer') | has('land surveyor') | has('architect') | has('urban planner')) & "
                                 "(yrs_career >= 4)", rate=0.086),
    # food and care: the commonest papers, kept while the work lasts
    "food hygiene certificate": dict(req="has('cook') | has('head chef') | has('baker') | has('community-kitchen volunteer') | "
                                         "has('care worker') | has('shop owner') | "
                                         "((has('waiter or bartender') | has('shop assistant')) & chance(.5))",
                                     rate=0.027, lrate=0.3,
                                     lose="~has('cook') & ~has('head chef') & ~has('baker') & "
                                          "~has('community-kitchen volunteer') & ~has('care worker') & ~has('shop owner') & "
                                          "~has('waiter or bartender') & ~has('shop assistant') & "
                                          "(yrs_has('food hygiene certificate') >= 3)",
                                     lwhy="out of date after years away from food work"),
    "cleared to work with children": dict(req="(age >= 16) & ~has('someone with a record') & (has('teacher') | "
                                              "has('youth coach') | has('foster parent') | has('adoptive parent') | "
                                              "has('school-governance board member') | has('lay religious teacher') | "
                                              "has('parent-association organiser') | has('guardian of an unrelated child') | "
                                              "has('nurse') | has('paramedic') | has('physician') | has('midwife') | "
                                              "(kids_home & chance(.1)) | (held_community & chance(.05)))",
                                          rate=0.045, lrate=0.5,
                                          lose="has('someone with a record') & (yrs_has('someone with a record') < 1)",
                                          lwhy="a new conviction showed on the check"),
    "lifeguard qualification": dict(req="has('swimming') & (age >= 16) & (age <= 30) & (health > .6)", rate=0.0033,
                                    weight="colors", grants=["first-aid certificate"], lrate=0.4,
                                    lose="(age >= 26) & (yrs_has('lifeguard qualification') >= 2) & ~has('lifeboat volunteer')",
                                    lwhy="let it lapse"),
    # words, ceremonies and care of the mind: approvals that come with the work, and go with a conviction
    "tattoo licence": dict(req="has('tattoo artist')", rate=1.0, lose="~has('tattoo artist')", lrate=0.5,
                           lwhy="lapsed after leaving the trade"),
    "celebrant authorisation": dict(req="(has('civil celebrant') | has('ordained religious minister') | "
                                        "(has('public speaking') & had(['dancing at a wedding'], 1) & chance(.2))) & "
                                        "~has('someone with a record')",
                                    rate=0.4, lose="has('someone with a record')", lrate=0.5,
                                    lwhy="struck from the register"),
    "court interpreter accreditation": dict(req="(has('court interpreter') | (has('translator') & (yrs_career >= 3))) & "
                                                "~has('someone with a record') & (age >= 23)",
                                            rate=0.00017, lrate=1.0,
                                            lose=[("has('someone with a record')", "a conviction"),
                                                  ("~has('court interpreter') & ~has('translator')",
                                                   "lapsed after leaving the work")]),
    "press card": dict(req="has('journalist') & (yrs_career >= 1)", rate=0.11, lose="~has('journalist')", lrate=0.5,
                       lwhy="handed back after leaving journalism"),
    "therapy accreditation": dict(req="(has('psychotherapist') | ((has('nurse') | has('teacher') | has('care worker')) & "
                                      "has('calming people down') & (age >= 25) & chance(.1))) & ~has('someone with a record')",
                                  rate=0.8, lose="has('someone with a record')", lrate=0.5,
                                  lwhy="struck off the register"),
    "mediation accreditation": dict(req="(age >= 21) & (has('community-mediation volunteer') | "
                                        "has('restorative-justice advocate') | "
                                        "(has('calming people down') & held_career & (yrs_career >= 5) & chance(.1)))",
                                    rate=0.0062),
    # learning, travel and settling
    "diving certificate": dict(req="has('swimming') & (age >= 10) & (health > .5) & "
                                   "had(['a long-planned trip', 'a trip far from home', 'a day at the beach'], 1)",
                               rate=0.018, weight="colors"),
    "reader's ticket": dict(req="(age >= 16) & (has('finding things out') | has('graduate') | "
                                "had(['a parent dies', 'a grandparent dies', 'losing a grandparent', "
                                "'a long-lost relative finds you'], 3))", rate=0.0007, weight="colors"),
    "permanent residence": dict(req="((has('immigrant') & (yrs_has('immigrant') >= 3)) | "
                                    "(has('refugee') & (yrs_has('refugee') >= 3))) & "
                                    "~has('citizenship') & ~has('returned migrant')",
                                rate=0.13, lrate=1.0,
                                lose=[("has('citizenship')", "replaced by citizenship"),
                                      ("has('returned migrant')", "given up on going home")]),

    # ---------------- assets
    "hives of one's own": dict(req="(age >= 14) & (has('plot of land') | has('farmer') | has('growing food') | "
                                   "had(['a new hobby you cannot put down', 'tending an allotment'], 2))",
                               rate=0.00017, weight="colors", lrate=0.5,
                               lose=[("had(['a third of the hives dead after winter'], 1) & chance(.3)",
                                      "the colonies died out"),
                                     ("ago_move < 1", "nowhere to keep them after a move"),
                                     ("(age >= 80) | (health < .35)", "the boxes grew too heavy")]),
    "boat of one's own": dict(req="(age >= 16) & (money > .3) & (has('swimming') | has('hunting and fishing'))",
                              rate=0.015, weight="money"),
    "share in a fishing boat": dict(req="has('commercial fisher') & (yrs_career >= 3) & "
                                        "(has('savings') | has('family business') | has('inheritance'))",
                                    rate=1.0, lrate=0.4,
                                    lose=[("had(['financial ruin'], 1)", "sold to pay debts"),
                                          ("~has('commercial fisher')", "sold on leaving the sea")]),
    "studio of one's own": dict(req="(age >= 18) & (money > .2) & (has('tattoo artist') | has('sound engineer') | "
                                    "((has('drawing and painting') | has('musical instrument')) & chance(.3)))",   # 10-09 floors (Emren: rare titles reachable): .1 to .3
                                rate=0.033, weight="money"),
    "premises of one's own": dict(req="has('shop owner') | ((has('founder of a firm') | has('baker') | "
                                      "has('funeral director') | has('pharmacist') | has('veterinarian') | "
                                      "has('physician') | has('carpenter') | has('tattoo artist') | "
                                      "has('psychotherapist') | has('head chef')) & (money > .25) & chance(.2))",
                                  rate=0.23, weight="money", lrate=0.5,
                                  lose=[("had(['financial ruin'], 1)", "financial ruin"),
                                        ("~held_career", "the lease given up")]),
    "horse of one's own": dict(req="(age >= 6) & (money > .3) & (has('plot of land') | has('farmer') | "
                                   "has('handling animals') | had(['a pet of your own'], 10))", rate=0.02, weight="money"),
    "good telescope": dict(req="(age >= 10) & (has('amateur astronomer in a club') | ((has('finding things out') | "
                               "had(['more stars than anyone could count', 'the sun goes dark at noon', 'awe'], 2)) & "
                               "chance(.1)))", rate=0.008, weight="colors"),
    "period kit": dict(req="has('historical reenactment member')", rate=0.67),
    "stake in the firm": dict(req="held_career & (yrs_career >= 8) & (has('physician') | has('pharmacist') | "
                                  "has('veterinarian') | has('architect') | has('accountant') | has('civil engineer') | "
                                  "has('land surveyor') | has('funeral director') | has('founder of a firm') | "
                                  "has('inner circle at work') | has('family business'))",
                              rate=0.023, weight="money", lrate=0.5,
                              lose=[("~held_career", "bought out on leaving"),
                                    ("had(['financial ruin'], 1)", "the firm went under")]),
    "research grant": dict(req="(age >= 23) & (has('doctoral graduate') | has('archaeologist') | has('museum curator') | "
                               "has('professional conservator') | has('archivist') | "
                               "(has('graduate') & (mkn('learned a skill') >= 5) & chance(.1)))",
                           rate=0.0025, weight="practice", lrate=0.6,
                           lose=[("had(['the grant runs out in June'], 1)", "the grant ran out"),
                                 ("yrs_has('research grant') >= 3", "the money was spent")]),
    "collection of one's own": dict(req="(age >= 12) & (has('finding things out') | has('museum curator') | "
                                        "had(['a curiosity that will not let go', 'a new hobby you cannot put down', "
                                        "'an unexpected legacy'], 3))", rate=0.0027, weight="colors"),
    "tools of one's own": dict(req="(age >= 16) & (has('carpenter') | has('welder') | has('plumber') | has('electrician') | "
                                   "has('builder') | has('machinist') | has('building trade') | has('car mechanics'))",
                               rate=0.03, weight="money"),
    "camper van": dict(req="(age >= 21) & has('driving licence') & (money > .35) & "
                           "(has('parent of independent adult children') | has('retiree') | "
                           "had(['the itch to be somewhere else', 'a late chance to see the world', 'a long-planned trip'], 3))",
                       rate=0.024, weight="money", lrate=0.5,
                       lose=[("had(['the doctor says to stop driving'], 1)", "the doctor says to stop driving"),
                             ("had(['financial ruin'], 1)", "financial ruin"),
                             ("(money < .05) & (yrs_adj('poor') >= 1)", "sold in hard times")]),
    "secure tenancy": dict(req="(age >= 18) & (ago_move >= 1) & ~has('homeowner') & (((money < .2) & (ago_move >= 2)) | "
                               "has('homeless') | "
                               "has('housing-cooperative member') | has('displaced by a disaster') | "
                               "had(['losing the home'], 2))",
                           rate=0.0061, lrate=0.5,
                           lose=[("has('homeowner')", "bought a home of their own"),
                                 ("(ago_move < 1) & ~has('housing-cooperative member')", "given up on moving away"),
                                 ("(money < .01) & (yrs_adj('poor') >= 1) & chance(.2)", "evicted after months of arrears")]),
    # ---------------- p2_skills
    # ---------------- skills
    # trades and making
    "welding": dict(req="has('welder') | has('machinist') | has('car mechanics') | has('building trade') | has('farmer')",
                    rate=0.00099),
    "machining": dict(req="has('machinist') | (was('apprentice') & (mkn('learned a skill') >= 2)) | "
                          "(has('factory worker') & has('fixing things'))", rate=0.00026),
    "baking": dict(req="has('baker') | has('cook') | has('cooking for a crowd') | "
                       "had(['learning to cook for yourself', 'a holiday meal with the whole family'], 3)", rate=0.0029),
    "restoring old things": dict(req="has('professional conservator') | has('museum curator') | has('repair-cafe volunteer') | "
                                     "((has('fixing things') | has('sewing and mending')) & (age >= 25))", rate=0.00028),
    # sea, land and living things
    "navigation": dict(req="has('commercial pilot') | has('merchant seafarer') | has('search-and-rescue volunteer') | "
                           "has('lifeboat volunteer') | has('soldier') | has('scout or guide') | "
                           "had(['a weekend hike', 'a long walk alone'], 3)", rate=0.0025),
    "boat handling": dict(req="has('merchant seafarer') | has('commercial fisher') | has('lifeboat volunteer') | "
                              "has('hunting and fishing') | (has('swimming') & had(['a day at the beach', 'summer camp'], 2))",
                          rate=0.004),
    # sea legs come within weeks at sea and go within a year or two ashore
    "sea legs": dict(req="has('merchant seafarer') | has('commercial fisher') | has('lifeboat volunteer') | has('boat handling')",
                     rate=0.06,
                     lose="~(has('merchant seafarer') | has('commercial fisher') | has('lifeboat volunteer') | "
                          "has('boat handling'))", lrate=0.5, lwhy="years ashore"),
    "knowing the woods": dict(req="has('forester') | has('hunting and fishing') | has('scout or guide') | has('farmer') | "
                                  "had(['a weekend hike', 'a long walk alone'], 3)", rate=0.0013),
    "handling animals": dict(req="has('veterinarian') | has('farmer') | has('animal-shelter campaigner') | "
                                 "has('dog of one\\'s own') | has('cat of one\\'s own')", rate=0.002),
    "beekeeping": dict(req="has('professional beekeeper') | has('farmer') | has('hives of one\\'s own') | "
                           "((age >= 14) & had(['a new hobby you cannot put down', 'tending an allotment'], 3))", rate=0.00029),
    # words and records
    "interpreting": dict(req="has('court interpreter') | has('translator') | (has('second language') & "
                             "(has('immigrant') | has('refugee') | has('parent raising a child across languages')))", rate=0.00096),
    "editing": dict(req="has('book editor') | has('journalist') | has('doctoral graduate') | "
                        "(has('graduate') & (mkn('learned a skill') >= 3))", rate=0.00048),
    "reporting": dict(req="has('journalist') | has('community-radio presenter') | has('digital-rights advocate') | "
                          "(has('finding things out') & has('writing stories'))", rate=0.0013),
    "writing stories": dict(req="has('novelist') | (had(['inspiration strikes', 'the urge to make something', "
                                "'the notebooks come together'], 3) & (mkn('learned a skill') >= 2))", rate=0.00067),
    "archive research": dict(req="has('archivist') | has('museum curator') | has('archaeologist') | has('doctoral graduate') | "
                                 "(has('finding things out') & (age >= 40))", rate=0.00036),   # family historians start late
    # science and systems
    "lab work": dict(req="has('laboratory technician') | has('pharmacist') | has('physician') | has('veterinarian') | "
                         "has('doctoral graduate') | (has('graduate') & (age <= 30) & (mkn('learned a skill') >= 3))", rate=0.0051),
    "working with data": dict(req="has('data analyst') | has('accountant') | has('software developer') | "
                                  "has('cybersecurity analyst') | has('doctoral graduate') | "
                                  "(has('office clerk') & has('bookkeeping')) | (has('graduate') & (mkn('learned a skill') >= 3))",
                              rate=0.0025),
    "keeping systems secure": dict(req="has('cybersecurity analyst') | has('digital-rights advocate') | "
                                       "(has('writing code') & (mkn('learned a skill') >= 3))", rate=0.00029),
    # stage and sound
    "sound mixing": dict(req="has('sound engineer') | has('community-radio presenter') | has('amateur band member') | "
                             "has('congregation musician') | has('stage technician')", rate=0.002),
    "stagecraft": dict(req="has('stage technician') | has('festival organiser') | has('amateur band member') | "
                           "(had(['the school play'], 5) & has('fixing things') & (age <= 25))", rate=0.0031),
    "singing": dict(req="has('choir member') | has('congregation musician') | has('amateur band member') | "
                        "has('regular worshipper') | (age <= 14)", rate=0.0051),
    # people
    "counselling": dict(req="has('psychotherapist') | has('ordained religious minister') | has('prison visitor') | "
                            "(has('calming people down') & (mkn('helped someone in need') >= 3))", rate=0.00041),
    "leading a ceremony": dict(req="has('civil celebrant') | has('ordained religious minister') | has('funeral director') | "
                                   "has('lay religious teacher') | has('deacon or elder') | "
                                   "(has('public speaking') & had(['a memorial service for a friend'], 2))", rate=0.00074),
    "settling disputes": dict(req="has('community-mediation volunteer') | has('restorative-justice advocate') | has('union rep') | "
                                  "has('shift manager') | (has('calming people down') & (mkn('helped someone in need') >= 3))",
                              rate=0.0014),
    "organising people": dict(req="(held_community & (yrs_community >= 2)) | has('shift manager') | has('founder of a firm')",
                              rate=0.0022),
    "campaigning": dict(req="has('civil-liberties campaigner') | has('disability-rights organiser') | "
                            "has('digital-rights advocate') | has('animal-shelter campaigner') | has('activist in a cause') | "
                            "has('union rep') | has('party member') | "
                            "had(['a protest in your city', 'a protest to save the local hospital'], 3)", rate=0.00049),
    "handling red tape": dict(req="has('parent coordinating complex support needs') | has('carer for a parent') | "
                                  "has('caregiving partner') | has('immigrant') | has('asylum applicant') | "
                                  "has('founder of a firm') | has('shop owner') | had(['your first tax form and a stack of bills', "
                                  "'sorting out your will', 'a dispute over an inheritance'], 2)", rate=0.0022),
    # the body
    "emergency care": dict(req="has('paramedic') | has('firefighter') | has('search-and-rescue volunteer') | "
                               "has('lifeboat volunteer') | has('nurse') | has('physician') | has('midwife') | "
                               "has('police officer') | has('soldier') | (has('first-aid certificate') & mk('helped someone in need'))",
                           rate=0.00058),
    "strong stomach": dict(req="has('paramedic') | has('physician') | has('nurse') | has('midwife') | has('funeral director') | "
                               "has('sanitation worker') | has('firefighter') | has('veterinarian') | has('farmer') | "
                               "has('care worker') | has('soldier')", rate=0.069),
    # the body adjusts within a year of nights and readjusts within a year of days; tolerance falls after sixty
    "used to night shifts": dict(req="has('nurse') | has('paramedic') | has('emergency dispatcher') | has('police officer') | "
                                     "has('firefighter') | has('physician') | has('midwife') | has('care worker') | "
                                     "has('factory worker') | has('baker') | has('train driver') | has('merchant seafarer') | "
                                     "has('waiter or bartender') | has('cleaner') | has('postal worker')", rate=0.013,
                                 lose=[("~held_career", "nights given up"), ("age >= 60", "the nights grew harder with age")],
                                 lrate=0.3),
    "head for heights": dict(req="has('firefighter') | has('stage technician') | has('builder') | has('building trade') | "
                                 "has('electrician') | has('search-and-rescue volunteer') | "
                                 "(has('keeping fit') & mk('took a wild risk'))", rate=0.0018),
    "keeping fit": dict(req="has('on the team') | has('professional athlete') | has('firefighter') | has('soldier') | "
                            "has('police officer') | has('search-and-rescue volunteer') | has('boxing or martial arts') | "
                            "had(['a weekend hike', 'a band or a sport that takes over your life', 'a warning from the doctor'], 2)",
                        rate=0.009),

    # ---------------- standing
    "book in print": dict(req="has('novelist') | has('journalist') | has('doctoral graduate') | has('name in the field') | "
                              "(has('writing stories') & (age >= 25))", rate=0.0021, weight="practice"),
    "published research": dict(req="has('doctoral graduate') | has('physician') | has('archaeologist') | "
                                   "has('laboratory technician') | has('museum curator') | has('professional conservator') | "
                                   "has('veterinarian') | has('pharmacist')", rate=0.045, weight="practice"),
    # regulars follow the person, not the shop: lost with the work or a move
    "loyal clientele": dict(req="(has('tattoo artist') | has('baker') | has('plumber') | has('carpenter') | has('electrician') | "
                                "has('builder') | has('translator') | has('civil celebrant') | has('sound engineer') | "
                                "has('psychotherapist') | has('shop owner') | has('cleaner') | has('funeral director') | "
                                "has('accountant') | has('salesperson') | has('estate agent')) & (yrs_career >= 3)",
                            rate=0.02, weight="practice",
                            lose=[("~held_career", "the work given up"), ("ago_move < 1", "a move away from the clients")],
                            lrate=0.6),
    # an award is kept for life; only a scandal undoes it
    "award for bravery": dict(req="(has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                  "has('paramedic') | has('police officer') | has('soldier') | has('local hero')) & "
                                  "mk('took a wild risk', 2) & mk('helped someone in need', 2)", rate=0.011,
                              lose="had(['a public scandal'], 1)", lrate=0.5, lwhy="a public scandal"),
    "voice at the town hall": dict(req="has('local councillor') | has('school-governance board member') | has('urban planner') | "
                                       "has('residents\\' committee member') | has('neighbourhood-watch coordinator') | "
                                       "has('civil-liberties campaigner') | has('disability-rights organiser') | "
                                       "(has('good name in town') & (yrs_community >= 3))", rate=0.0029, weight="colors",
                                   lose=[("ago_move < 1", "a move away"),
                                         ("had(['a public scandal', 'a bitter election'], 1)", "a scandal or a bitter election")],
                                   lrate=0.6),
    "name on the local scene": dict(req="has('amateur band member') | has('festival organiser') | has('community-radio presenter') | "
                                        "has('tattoo artist') | has('sound engineer') | has('head chef') | "
                                        "has('board-game club organiser')", rate=0.0073, weight="colors",
                                    lose=[("ago_move < 1", "a move to a new town"),
                                          ("~held_community & ~held_career", "out of the scene")], lrate=0.5),
    "trusted with the keys": dict(req="(age >= 18) & (has('reliable record') | has('cleaner') | has('postal worker') | "
                                      "has('club treasurer') | has('deacon or elder') | has('lay religious teacher') | "
                                      "has('neighbourhood-watch coordinator') | has('housing-cooperative member'))",
                                  rate=0.008, weight="colors",
                                  lose=[("mk('broke your word', 1) | mk('hid a wrong', 1)", "trust broken"),
                                        ("ago_move < 1", "a move away")], lrate=0.5),
    "trophies won": dict(req="(has('on the team') & (yrs_has('on the team') >= 2)) | has('team captain') | "
                             "has('professional athlete') | has('boxing or martial arts')", rate=0.0021, weight="practice"),

    # ---------------- bonds
    # the crew of the job held now; once the job is left, what remains is old comrades
    "crew that has your back": dict(req="has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                        "has('merchant seafarer') | has('commercial fisher') | has('stage technician') | "
                                        "has('paramedic') | has('police officer') | has('soldier') | has('head chef') | "
                                        "has('cook') | has('sanitation worker') | has('builder')", rate=0.05, weight="ties",
                                    lose="~(has('firefighter') | has('lifeboat volunteer') | has('search-and-rescue volunteer') | "
                                         "has('merchant seafarer') | has('commercial fisher') | has('stage technician') | "
                                         "has('paramedic') | has('police officer') | has('soldier') | has('head chef') | "
                                         "has('cook') | has('sanitation worker') | has('builder'))",
                                    lrate=0.5, lwhy="the crew left behind"),
    # an apprenticeship runs three or four years; then the apprentice goes
    "apprentice of one's own": dict(req="(age >= 25) & (yrs_career >= 5) & (has('machinist') | has('welder') | has('plumber') | "
                                        "has('carpenter') | has('electrician') | has('builder') | has('baker') | has('head chef') | "
                                        "has('tattoo artist') | has('farmer') | has('professional beekeeper'))",
                                    rate=0.035, weight="practice",
                                    lose="yrs_has('apprentice of one\\'s own') >= 4", lrate=0.5,
                                    lwhy="the apprentice qualified and went their own way"),
    "carers' group": dict(req="has('carer for a parent') | has('caregiving partner') | "
                              "has('parent coordinating complex support needs') | has('grandparent raising a grandchild')",
                          rate=0.0046, weight="ties",
                          lose="~(has('carer for a parent') | has('caregiving partner') | "
                               "has('parent coordinating complex support needs') | has('grandparent raising a grandchild'))",
                          lrate=0.3, lwhy="the caring years over"),
    "source who trusts you": dict(req="has('journalist') | has('digital-rights advocate') | has('civil-liberties campaigner')",
                                  rate=0.0085, weight="ties",
                                  lose=[("mk('broke your word', 1)", "a confidence broken"),
                                        ("~(has('journalist') | has('digital-rights advocate') | has('civil-liberties campaigner'))",
                                         "out of the work")], lrate=0.5),
    "business partner": dict(req="(age >= 18) & (has('founder of a firm') | has('shop owner') | has('plumber') | has('carpenter') | "
                                 "has('tattoo artist') | has('architect') | has('accountant') | has('psychotherapist') | "
                                 "has('estate agent') | has('farmer'))", rate=0.061, weight="money",
                             lose=[("had(['betrayed by a friend or a business partner', 'financial ruin'], 1)", "a betrayal or a ruin"),
                                   ("~held_career", "the business wound up")], lrate=0.6),
    "godchild": dict(req="(age >= 16) & (mkn('made a friend') >= 2) & (has('friend for life') | has('regular worshipper') | "
                         "has('believer on the big days'))", rate=0.0031, weight="ties"),
    "cat of one's own": dict(req="had(['a pet of your own'], 1) | (age >= 18)", rate=0.01,
                             lose="had(['your pet dies'], 1)", lrate=1.0, lwhy="the cat died"),
    "people from home": dict(req="has('immigrant') | has('refugee') | has('asylum applicant') | "
                                 "((ago_move < 3) & (mkn('moved away') >= 1))", rate=0.0063, weight="ties"),
}

TITLE_LINKS = {
    'train driver': dict(grants=['train driving licence'], lrate=1.0, lose=[("~has('train driving licence')", 'lost the train driving licence')], why="the operator's training gives the licence; a failed medical or a conviction ends the licence, and the cab goes with it"),
    'commercial pilot': dict(grants=['airline pilot licence', 'navigation'], lrate=1.0, lose=[("~has('airline pilot licence') & (age < 65)", 'lost the licence')], why='the licence comes with the first commercial post; a failed medical ends the licence, and at 65 the title ends by age as before; years of flight training come before a first commercial post'),
    'merchant seafarer': dict(grants=["seafarer's papers", 'sea survival certificate'], lrate=1.0, lose=[("~has('seafarer\\'s papers')", "lost the seafarer's papers")], why='the cadetship gives the papers and the survival course; a failed seafarer medical ends the papers and the sea career'),
    'court interpreter': dict(grants=['court interpreter accreditation', 'interpreting'], lrate=1.0, lose=[("~has('court interpreter accreditation')", 'lost accreditation')], why="accreditation comes with the first court list; a conviction ends it (as the title's old lose did) and the court work with it; an interpreting qualification comes before accreditation"),
    'civil celebrant': dict(req="(age >= 25) & has('public speaking') & ~has('someone with a record')", grants=['celebrant authorisation', 'leading a ceremony'], lrate=1.0, lose=[("~has('celebrant authorisation')", 'lost authorisation')], why='registration asks for a fit and proper person; struck from the register, the celebrant stops; a celebrant course comes before the first booking'),
    'psychotherapist': dict(req="has('graduate') & (age >= 25) & ~has('someone with a record')", grants=['therapy accreditation', 'counselling'], lrate=1.0, lose=[("~has('therapy accreditation')", 'lost accreditation')], why='the training ends in accreditation; struck off, the therapist closes the practice; a long training with supervised clients comes before a caseload'),
    'professional beekeeper': dict(req="(age >= 20) & (mkn('learned a skill') >= 3) & has('hives of one\\'s own')", lrate=1.0, lose=[("~has('hives of one\\'s own')", 'the hives were lost or sold')], why="the business grows from a few hives of one's own; without hives it ends; years of beekeeping practice come before hundreds of hives", grants=['beekeeping']),
    'amateur astronomer in a club': dict(req="(age >= 10) & (had(['more stars than anyone could count', 'the sun goes dark at noon', 'awe'], 10) | has('finding things out') | has('good telescope'))", why='an owner of a good telescope often looks for a club to share the sky with; the telescope is one way in, never required'),
    'commercial fisher': dict(grants=['sea survival certificate', 'fishing licence'], why='sea safety training and a licence come with the first berth'),
    'lifeboat volunteer': dict(grants=['sea survival certificate'], why='sea survival is part of crew training'),
    'welder': dict(grants=['welding certificate', 'welding'], why='the coded test is how a welder is taken on; coded tests are passed before the first job'),
    'tattoo artist': dict(grants=['tattoo licence'], why='the council registers the artist with the studio'),
    'forester': dict(grants=['chainsaw ticket', 'knowing the woods'], why='forestry training includes the chainsaw ticket; a forestry degree or apprenticeship comes first'),
    'community-mediation volunteer': dict(grants=['mediation accreditation', 'settling disputes'], why="the service's training course ends in accreditation; a training course comes before supervised mediation"),
    'ordained religious minister': dict(grants=['celebrant authorisation', 'leading a ceremony'], why='in most traditions ordination lets a minister conduct weddings; years of training come before ordination'),
    'baker': dict(grants=['food hygiene certificate', 'baking'], why='no bakery opens its ovens to the untrained; early shifts as a bakery assistant come before responsibility for the bake'),
    'cook': dict(grants=['food hygiene certificate'], why='every commercial kitchen trains its staff in food hygiene'),
    'community-kitchen volunteer': dict(grants=['food hygiene certificate'], why='the induction includes food-safety training'),
    'laboratory technician': dict(grants=['lab work'], why='a technical course or a science degree, and safety training, come first'),
    'paramedic': dict(grants=['emergency care'], why='a paramedic degree with supervised ambulance placements comes first'),
    'veterinarian': dict(grants=['handling animals'], why='five or six years of veterinary school come first'),
    'firefighter': dict(grants=['keeping fit'], why='fitness tests are passed before a place on a watch'),
    'journalist': dict(grants=['reporting'], why='a journalism course or a student paper comes before a first commission'),
    'book editor': dict(grants=['editing'], why="years as an editorial assistant come before a list of one's own"),
    'archivist': dict(grants=['archive research'], why='archival training or proven competence comes first'),
    'data analyst': dict(grants=['working with data'], why='the workplace takes them on to turn records into answers'),
    'cybersecurity analyst': dict(grants=['keeping systems secure'], why='certifications come before a post on a security team'),
    'machinist': dict(grants=['machining'], why="machine training comes before jobs of one's own on the lathes and mills"),
    'sound engineer': dict(grants=['sound mixing'], why='audio skill comes before paid sessions'),
    'stage technician': dict(grants=['stagecraft'], why='a venue or a crew takes on someone who already knows the work'),
    'professional athlete': dict(grants=['keeping fit'], why='years of academies and tryouts come before a contract'),
    'novelist': dict(grants=['writing stories'], why='a long writing practice comes before the first published book'),
    'professional conservator': dict(grants=['restoring old things'], why='a conservation degree and internships come first'),
    'search-and-rescue volunteer': dict(grants=['navigation'], why='a probationary year of training comes before a place on the team'),
}

ROLES.update(ROLES_V2)
ROLES.update(ROLES_P2)
for t_, r_ in TITLE_LINKS.items():
    d_ = dict(ROLES.get(t_) or {})
    for k_, v_ in r_.items():
        if k_ == "grants":
            d_["grants"] = list(d_.get("grants", [])) + [g_ for g_ in v_ if g_ not in d_.get("grants", [])]
        elif k_ != "why":
            d_[k_] = v_
    ROLES[t_] = d_
# only ever through an act (the packs, 07:21): a failed long shot (grants_if_fails), so every holder has a real scene behind
# it for the Book, the peace reading and the echoes; rate 0 means no draw "in time", and the rate fit leaves it out
ROLES_ACTS_ONLY = {"a long shot that missed": dict(rate=0)}
# One budget for big lives across all the packs on (Emren, pack ideas thread, relayed 08:14): about 1 life in 3 holds a big
# career and about 1 in 20 reaches a summit; community titles at 10x their real share, capped at 1 in 4 (batch.TARGET_CAP).
# Pack titles join a tier through the tier words in TARGET_<PACK> (batch._targets).
# Emren 10-09: "0.1% is not playable. Rare titles must be more reachable": every summit in 1 life in 100 or more (the
# summit budget from 1 in 20 to about 1 in 7 to hold ten to twelve of them), every career above 1 in 100 (1.5%), and
# every other title of one's own doing and every perk in 1 life in 100 or more (batch._targets). Statuses keep their
# real shares: what befalls a life (refugee, widowed) is not a prize to make reachable.
BUDGET = dict(career=1 / 3, summit=0.15, community=10.0, summit_floor=0.01,   # each summit in 1 life in 100 or more
              career_floor=0.015, title_floor=0.01, perk_floor=0.01,
              perk_floor_rel=0.5,     # a perk that needs a title: at most 1 in 2 of what its titles allow (10-09)
              summit_per_pack=0.05,   # each pack's summits share 1 in 20 lives of their own (10-09)
              rung_cap=2.0,   # the lift raises a rung's yearly rate by at most e^2, about 7x (was e^1; Emren 10-09)
              act_cap=1.2)    # and the odds of an act that gives one by at most e^1.2, about 3x (was e^.7, about double,
                              # Emren 14:41; raised 10-09 so the 1-in-100 summit floor can be reached)
# The fitted logit lift per tier, on the odds of the acts that give a pack career or summit and on their background rates,
# per set of packs on (",".join(sorted(packs))); "split": the extra lift per summit that brings each to its share of the
# summit budget (the square root of its real share). calib_v8/tier_fit.py writes it.
TIER_LIFT = {
    'politics,science,stage': {"career": 3.2034, "split": {"artistic director": 5.3746, "campaign organiser": -2.7012, "casting director": 6.0, "constituency caseworker": -3.2683, "director": -0.433, "drama teacher": -2.0937, "evidence synthesis specialist": 0.0148, "head of government": 6.0, "independent investigator": -5.4576, "lead actor or actress": -5.6001, "lobbyist": -2.3756, "mayor": -5.4931, "member of parliament": 5.4332, "minister": 6.0, "participatory research coordinator": 6.0, "party leader": 6.0, "party official": -0.9324, "playwright or screenwriter": 0.4191, "policy analyst": 1.1261, "political adviser": -0.2837, "pollster": 6.0, "postdoctoral researcher": 4.2211, "producer": 1.8658, "professional actor": -2.4741, "professor": 0.082, "research assistant": -2.8835, "research data steward": 3.8182, "research facility lead": -2.9888, "research group leader": -3.2429, "research project lead": -3.095, "research scientist": -4.1457, "research software engineer": 4.3164, "science communication specialist": -0.3194, "speechwriter": 5.349, "stage manager": -0.6015, "talent agent": 6.0, "voice actor": 5.1045}, "summit": 8.0},
}
ROLES.update(ROLES_ACTS_ONLY)
ROLES_OPTIONAL = set(ROLES_V2) | set(ROLES_P2) | set(ROLES_ACTS_ONLY)   # chroma-packs/core/longshot.py: only with packs on
ROLES = {k_: v_ for k_, v_ in ROLES.items() if v_ is not None and k_ == k_.strip()}
# measured multipliers so each item's lifetime share matches the catalogue (calib_v7/roles_check.py; pack fit science,politics,stage, 10-07 06:21, after the tier lift);
# entry titles are weights among a commitment's first titles
ROLE_NORM = {
    'a campaign war chest': 0.134, 'a casting eye': 1.36, 'a company of your own': 2.287,
    'a company that feels like family': 0.121, 'a cult following': 60.0, 'a dataset others use': 8.931,
    'a director who keeps casting you': 2.703, 'a finding that held up': 0.005, 'a following in the party': 2.377,
    'a fringe slot': 1.767, 'a household name': 60.0, 'a known face': 60.0, 'a lead role to remember': 0.007,
    'a list of supporters': 3.173, 'a loyal campaign team': 0.067, 'a loyal research team': 0.455,
    'a method others use': 1.797, 'a movement behind you': 0.649, 'a name as a fixer': 43.594,
    'a name for straight talk': 0.005, 'a nose for the odd result': 0.005, 'a parliamentary pass': 0.049,
    'a producer who backs you': 1.681, 'a reform with your name on it': 4.662, 'a research project under way': 0.022,
    'a safe seat': 60.0, 'a showreel': 60.0, 'a year group from drama school': 2.48, 'accents and voices': 0.259,
    'accountant': 0.287, 'acting': 1.057, 'activist in a cause': 0.005, 'adopted person': 14.353,
    'adoptive parent': 0.813, 'allies in the party': 0.005, 'amateur actor': 0.877,
    'amateur astronomer in a club': 0.03, 'amateur band member': 0.089, 'an agent who believes in you': 0.615,
    'an award for acting': 1.341, 'animal-shelter campaigner': 0.411, 'apprentice': 0.128,
    "apprentice of one's own": 0.754, 'archaeologist': 2.311, 'architect': 60.0, 'archive research': 1.144,
    'archivist': 1.108, 'asylum applicant': 0.613, 'auditioning': 2.649, 'automating analysis': 0.242,
    'award for bravery': 2.941, 'background artist': 0.005, 'baker': 0.012, 'baking': 0.636,
    'bankruptcy or insolvency in their history': 0.371, 'beekeeping': 3.984, 'believer on the big days': 0.099,
    'board-game club organiser': 0.039, 'boat handling': 0.013, "boat of one's own": 0.97, 'book editor': 0.384,
    'book in print': 0.433, 'book-club organiser': 0.296, 'bookkeeping': 0.064, 'boxing or martial arts': 0.108,
    'builder': 0.186, 'building trade': 0.215, 'business partner': 1.22, 'calling the show': 0.07,
    'calming people down': 0.214, 'campaign volunteer': 0.095, 'campaigning': 0.057, 'camper van': 0.612,
    'cancer survivor': 5.2, 'canvassing': 0.005, 'car': 2.462, 'car mechanics': 0.428, 'cards for money': 0.291,
    'care worker': 0.83, 'caregiving partner': 0.01, 'carer for a parent': 0.059, "carers' group": 0.494,
    'carpenter': 0.073, 'casting directory listing': 0.108, "cat of one's own": 0.864,
    'celebrant authorisation': 0.511, 'chainsaw ticket': 0.327, 'chartered status': 0.558,
    'child performance licence': 1.369, 'choir member': 0.037, 'citizen scientist': 0.14, 'citizenship': 0.014,
    'civil celebrant': 2.857, 'civil engineer': 0.215, 'civil-liberties campaigner': 0.068, 'cleaner': 0.423,
    'cleared to work with children': 1.17, 'club treasurer': 6.76, 'coaching badge': 0.107,
    'coalition building': 0.005, "collection of one's own": 0.684, 'commercial fisher': 1.587,
    'commercial pilot': 0.781, 'community listening': 0.086, 'community observer': 0.984, 'community partners': 0.469,
    'community theatre director': 0.031, 'community-garden coordinator': 0.095, 'community-kitchen volunteer': 0.005,
    'community-mediation volunteer': 0.516, 'community-radio presenter': 0.124, 'congregation musician': 0.298,
    'constituency casework': 0.005, 'contact in the trade': 0.426, 'convert': 9.205, 'cook': 2.68,
    'cooking for a crowd': 0.797, 'council candidate': 0.009, 'counselling': 0.156, 'counting the votes': 34.25,
    'court interpreter': 4.079, 'court interpreter accreditation': 1.127, 'credit negotiation': 0.005,
    'crew that has your back': 0.715, 'cybersecurity analyst': 18.574, 'dancing': 0.387, 'data analyst': 0.056,
    'deacon or elder': 1.148, 'debating': 1.969, 'delivery driver': 0.041, 'digital-rights advocate': 0.488,
    'directing actors': 0.75, 'disability-rights organiser': 0.078, 'displaced by a disaster': 0.873,
    'diving certificate': 1.182, 'doctoral graduate': 0.024, "dog of one's own": 0.586, 'donors': 60.0,
    'drafting policy': 0.097, 'drama school diploma': 0.035, 'drama school student': 0.18,
    'drawing and painting': 0.223, 'drinks licence': 0.005, 'driving licence': 0.862, 'editing': 0.131,
    'eldest child': 15.144, 'electrician': 0.68, 'emergency care': 0.108, 'emergency dispatcher': 0.015,
    'engaged': 0.186, 'estate agent': 0.098, 'ethics approval': 1.14, 'evidence synthesis': 0.138,
    'ex-prisoner': 0.606, 'experimental design': 0.005, 'explaining science': 0.005, 'factory worker': 0.48,
    'family abroad': 1.491, 'family business': 0.856, 'family who will always take you in': 2.125, 'farmer': 5.735,
    'festival organiser': 0.058, 'field permit': 60.0, 'fieldwork': 0.005, 'finding things out': 0.571,
    'firefighter': 0.182, 'first-aid certificate': 0.005, 'first-generation university student': 0.588,
    'fishing licence': 2.683, 'fixing things': 0.567, 'flat to rent out': 48.781, 'following online': 0.268,
    'food hygiene certificate': 0.626, 'forester': 3.609, 'former foster child': 0.104, 'former students': 0.432,
    'foster parent': 5.062, 'founder of a firm': 0.01, 'friend for life': 0.413, 'friend in power': 0.005,
    'friends across the aisle': 9.33, 'fundraising': 0.351, 'funeral director': 0.359,
    'gas safety registration': 1.56, 'girlfriend or boyfriend': 60.0, 'godchild': 0.005,
    'godparent who looks out': 0.874, 'good credit': 0.135, 'good name in town': 0.162, 'good notices': 2.114,
    'good telescope': 0.921, 'graduate': 0.687, 'grandparent': 0.55, 'grandparent raising a grandchild': 3.353,
    'grant writing': 0.005, 'growing food': 1.464, 'guardian of an unrelated child': 0.102, 'handling animals': 0.572,
    'handling red tape': 6.906, 'handling the press': 0.005, 'has killed in war': 0.693, 'has taken a life': 0.005,
    'head chef': 0.477, 'head for heights': 1.118, 'head of government': 60.0, 'historical reenactment member': 0.161,
    "hives of one's own": 3.051, 'home nursing': 0.046, 'home-educating parent': 0.028, 'homeless': 0.161,
    'homeowner': 0.996, "horse of one's own": 1.01, 'housing-cooperative member': 0.118, 'hunting and fishing': 0.356,
    'hunting licence': 0.115, 'immigrant': 0.159, 'improvisation': 0.319, 'in a street gang': 0.597,
    'in recovery': 0.235, 'in-laws who took you in': 0.007, 'inheritance': 0.333, 'inner circle at work': 0.289,
    "instrument of one's own": 0.716, 'instrument time': 11.352, 'instrument troubleshooting': 0.032,
    'interfaith-dialogue participant': 0.005, 'interpreting': 0.118, 'journalist': 0.235, 'keeping fit': 2.094,
    'keeping systems secure': 0.64, 'knowing every street': 0.005, 'knowing the rules of the house': 14.131,
    'knowing the woods': 0.005, 'known across the country': 0.647, 'known face at worship': 0.388, 'lab work': 0.005,
    'laboratory technician': 0.01, 'land surveyor': 0.862, 'lay religious teacher': 0.049,
    'leading a ceremony': 0.157, 'learning lines': 0.31, 'lifeboat volunteer': 0.007,
    'lifeguard qualification': 1.395, 'living in residential care': 10.981, 'living together': 0.188,
    'local councillor': 0.005, 'local hero': 0.406, 'local party officer': 13.391, 'lorry or bus licence': 0.784,
    'loyal clientele': 0.005, 'machining': 0.478, 'machinist': 0.021, 'mediation accreditation': 0.961,
    'member of a monastic community': 10.442, 'mentor': 0.033, 'merchant seafarer': 0.363, 'midwife': 18.749,
    'minding small children': 0.126, 'motorbike licence': 0.57, 'museum curator': 1.714, 'musical instrument': 0.06,
    'name in the field': 0.257, 'name on the local scene': 0.506, 'navigation': 1.61,
    'neighbour who has your back': 0.249, 'neighbourhood volunteer': 0.153, 'neighbourhood-watch coordinator': 0.195,
    'nonromantic life partner': 1.209, 'not to be crossed': 0.006, 'novelist': 0.234, 'nurse': 13.625,
    'office clerk': 0.159, 'officials who trust you': 3.548, 'old comrades': 0.275, 'old family name': 4.017,
    'old school network': 0.09, 'on probation or community supervision': 0.368, 'on the team': 0.434,
    'ordained religious minister': 2.564, 'organising people': 0.005, 'paid-off home': 0.982, 'paramedic': 24.552,
    'parent coordinating complex support needs': 1.167, 'parent of an only child': 0.058,
    'parent of independent adult children': 0.093, 'parent of three or more': 1.102,
    'parent raising a child across languages': 0.409, 'parent with a child living abroad': 0.947,
    'parent-association organiser': 0.126, 'parliamentary candidate': 9.706, 'parliamentary nomination': 60.0,
    'partner in a multigenerational household': 0.916, 'partner of many years': 0.12, 'party leader': 60.0,
    'party member': 0.02, 'passport': 0.292, 'patron': 0.12, 'people from home': 0.391, 'period kit': 33.144,
    'permanent residence': 0.022, 'pharmacist': 34.837, 'physician': 10.123, 'place by the sea': 4.398,
    'plot of land': 60.0, 'plumber': 0.221, 'police officer': 0.312, 'polling-station volunteer': 0.016,
    'postal worker': 0.015, 'prefect': 0.883, "premises of one's own": 0.832, 'press card': 36.665,
    'prison visitor': 0.487, 'professional athlete': 11.575, 'professional beekeeper': 60.0,
    'professional conservator': 3.022, 'professional registration': 0.274, 'project triage': 0.548,
    'psychotherapist': 0.237, 'public speaking': 0.133, 'published research': 0.005,
    'qualitative interpretation': 0.308, 'rank': 2.294, "reader's ticket": 1.011, 'reading the polls': 60.0,
    "referee's badge": 0.204, 'refugee': 0.953, 'regular at the local': 0.162, 'regular worshipper': 0.034,
    'reliable record': 0.111, 'repair-cafe volunteer': 0.005, 'repeat fees': 46.102, 'reporting': 2.357,
    'reproducible workflow': 0.005, 'research collaborators': 0.005, 'research grant': 0.005,
    'research integrity': 0.005, "residents' committee member": 0.652, 'restorative-justice advocate': 0.171,
    'restoring old things': 2.106, 'returned migrant': 0.125, 'rigging ticket': 0.965, 'rousing a crowd': 5.167,
    'salesperson': 4.142, 'sanitation worker': 0.063, 'savings': 0.137, 'scholarship': 0.364,
    'school-governance board member': 0.194, 'school-leaving certificate': 0.721, 'scout or guide': 0.614,
    'screen acting': 5.345, 'scripture': 0.068, 'sea legs': 1.115, 'sea survival certificate': 0.005,
    "seafarer's papers": 0.878, 'search-and-rescue volunteer': 0.07, 'second language': 0.286,
    'secure tenancy': 1.505, 'seeker': 0.272, 'selling': 0.383, 'settling disputes': 0.381,
    'sewing and mending': 0.287, 'shares': 13.774, 'shift manager': 0.005, 'shop assistant': 3.435,
    'shop owner': 0.011, 'singing': 0.97, 'single parent': 0.335, 'site safety card': 0.756,
    'software developer': 11.051, 'soldier': 0.17, 'someone with a record': 0.005, 'sound engineer': 0.114,
    'sound mixing': 0.828, 'source who trusts you': 2.726, 'sponsor in recovery': 0.021, 'sports referee': 0.048,
    'spouse in a family-arranged marriage': 0.635, 'stage combat': 1.458, 'stage technician': 0.01,
    'stagecraft': 0.005, 'stake in the firm': 0.82, 'statistical judgment': 12.396, 'stepparent': 1.373,
    'striking a deal': 0.389, 'strong stomach': 0.876, "studio of one's own": 1.051, 'supervising researchers': 0.005,
    'swimming': 1.268, 'tattoo artist': 9.842, 'teacher': 1.031, "teachers' favourite": 0.776, 'teaching': 0.005,
    'team captain': 0.153, 'telling a story aloud': 2.903, 'the one everyone asks': 0.218,
    'therapy accreditation': 0.18, "tools of one's own": 1.047, 'trade ticket': 0.064, 'train driver': 0.395,
    'translator': 0.83, 'trophies won': 0.918, 'trusted with the keys': 0.005, 'understudy': 13.401,
    'union card': 0.248, 'union rep': 0.005, 'urban planner': 2.581, 'used to night shifts': 0.715,
    'van and tools': 3.743, 'veterinarian': 60.0, 'video-game developer': 2.558, 'voice at the town hall': 1.047,
    'volunteer research organiser': 0.436, 'waiter or bartender': 3.428, 'welder': 0.02, 'welding': 1.288,
    'welding certificate': 0.094, 'working with data': 0.697, 'workplace pension': 0.353, 'workshop': 0.954,
    'writing code': 0.231, 'writing scripts': 0.072, 'writing speeches': 15.159, 'writing stories': 0.918,
    'youth coach': 0.16, 'youth theatre member': 6.059,
}


ROLE_ACC_FIRST = {
    'architect': 0.896,
    'care worker': 0.476,
    'cleaner': 0.398,
    'convert': 0.123,
    'cook': 0.481,
    'factory worker': 0.428,
    'salesperson': 0.509,
    'seeker': 0.395,
    'shop assistant': 0.429,
    'veterinarian': 0.745,
    'waiter or bartender': 0.686,
}

# acceptance by route (roles_check.py FIT_ACC): a title one route overfills is taken that way less often
ROLE_ACC_MOVE = {
    'accountant': 0.64,
    'apprentice': 0.438,
    'archaeologist': 0.355,
    'architect': 0.092,
    'civil celebrant': 0.331,
    'civil engineer': 0.537,
    'commercial fisher': 0.331,
    'delivery driver': 0.603,
    'estate agent': 0.34,
    'farmer': 0.543,
    'firefighter': 0.525,
    'founder of a firm': 0.548,
    'funeral director': 0.265,
    'journalist': 0.201,
    'laboratory technician': 0.11,
    'land surveyor': 0.331,
    'merchant seafarer': 0.578,
    'nurse': 0.451,
    'office clerk': 0.638,
    'paramedic': 0.525,
    'pharmacist': 0.241,
    'physician': 0.174,
    'police officer': 0.477,
    'postal worker': 0.425,
    'professional athlete': 0.191,
    'sanitation worker': 0.304,
    'shop owner': 0.21,
    'software developer': 0.887,
    'soldier': 0.345,
    'sound engineer': 0.256,
    'stage technician': 0.034,
    'tattoo artist': 0.239,
    'train driver': 0.418,
    'translator': 0.141,
    'urban planner': 0.138,
    'veterinarian': 0.745,
}









# The Library's chance per option (point 8): skill, world push and perks per color (W U B R G) of the people who meet
# each moment, measured on 600 lives of the staged batch (calib_v7/chance_check.py measure, 2026-10-05). load_batch sets
# each option's difficulty from it so its true odds for them come to its chance. Moments missing here use the mean.
CHANCE_REF = {
    'a performance review': (0.662, 0.554, 0.414, 0.690, 0.472),
    "a neighbour's dog keeps you awake": (0.724, 0.560, 0.428, 0.669, 0.537),
    'a rival at work': (0.650, 0.560, 0.434, 0.640, 0.508),
    "a child's birthday party in the family": (0.581, 0.505, 0.408, 0.581, 0.496),
    'a big night out after years of routine': (0.559, 0.532, 0.416, 0.603, 0.466),
    'the house needs repairs': (0.631, 0.557, 0.419, 0.722, 0.552),
    'a weekend with nothing planned': (0.571, 0.511, 0.394, 0.625, 0.468),
    'a budget that will not balance': (0.660, 0.547, 0.449, 0.623, 0.560),
    'a holiday dinner with both families': (0.641, 0.517, 0.415, 0.734, 0.499),
    'someone at work flirts with you': (0.607, 0.562, 0.426, 0.664, 0.492),
    'a bonus or a raise': (0.567, 0.502, 0.408, 0.559, 0.468),
    'you feel stuck and restless': (0.613, 0.537, 0.421, 0.597, 0.521),
    'new technology changes your job': (0.643, 0.554, 0.422, 0.748, 0.507),
    'a parent comes to stay for a week': (0.614, 0.515, 0.428, 0.729, 0.493),
    'a chance to make money on the side, not quite legal': (0.606, 0.540, 0.412, 0.585, 0.500),
    'a friend wants to start a project with you': (0.649, 0.575, 0.430, 0.594, 0.491),
    'you see a stranger being harassed': (0.610, 0.567, 0.449, 0.647, 0.497),
    'a quiet evening at home': (0.622, 0.511, 0.409, 0.543, 0.477),
    'a child in the family learns to ride a bike': (0.584, 0.543, 0.445, 0.611, 0.495),
    'your team lands a big contract': (0.639, 0.519, 0.422, 0.606, 0.500),
    'getting married': (0.624, 0.561, 0.426, 0.677, 0.499, 0.006),
    'a child is born': (0.600, 0.524, 0.407, 0.624, 0.511),
    'burnout': (0.651, 0.579, 0.502, 0.651, 0.539),
    'a serious accident or illness': (0.704, 0.563, 0.440, 0.626, 0.566),
    'buying a home': (0.674, 0.495, 0.398, 0.581, 0.527),
    'a chance to start a business of your own': (0.679, 0.554, 0.405, 0.607, 0.520),
    'your child falls seriously ill': (0.763, 0.529, 0.423, 0.541, 0.561),
    'your child dies': (0.738, 0.507, 0.411, 0.506, 0.581),
    'the first night away from home': (0.596, 0.640, 0.575, 0.609, 0.592),
    'voices raised downstairs after bedtime': (0.610, 0.644, 0.581, 0.626, 0.594),
    'nobody to play with at break time': (0.600, 0.636, 0.592, 0.608, 0.579),
    'the sibling who always gets more': (0.564, 0.593, 0.566, 0.593, 0.538),
    'the same bad dream again': (0.587, 0.595, 0.568, 0.582, 0.536),
    'a dare from the big kids': (0.604, 0.642, 0.608, 0.674, 0.602),
    'in a hurry to be grown up': (0.633, 0.656, 0.630, 0.658, 0.620),
    'a secret that wants to burst out': (0.622, 0.654, 0.587, 0.642, 0.609),
    'the lessons get hard': (0.607, 0.643, 0.596, 0.641, 0.590),
    'a best friend finds a new best friend': (0.607, 0.646, 0.589, 0.635, 0.591),
    'saving up for something big': (0.605, 0.647, 0.596, 0.627, 0.600),
    'the morning things feel better': (0.584, 0.623, 0.579, 0.624, 0.587),
    'a hero to be like': (0.609, 0.633, 0.614, 0.630, 0.602),
    'a den of your own': (0.586, 0.612, 0.579, 0.615, 0.582),
    'a promise kept all week': (0.614, 0.636, 0.589, 0.630, 0.610),
    'trusted with a grown-up job': (0.624, 0.649, 0.609, 0.640, 0.617),
    'bored on a rainy afternoon': (0.588, 0.614, 0.575, 0.619, 0.583),
    "a friend's new bike stings": (0.604, 0.631, 0.615, 0.627, 0.595),
    'a fib that will not stop nagging': (0.607, 0.656, 0.602, 0.657, 0.607),
    'everyone laughed when you got it wrong': (0.608, 0.646, 0.589, 0.641, 0.590),
    'an empty chair on a special day': (0.611, 0.646, 0.596, 0.633, 0.598),
    'a temper that keeps boiling over': (0.611, 0.627, 0.587, 0.667, 0.587),
    'the dark at the top of the stairs': (0.521, 0.544, 0.516, 0.516, 0.495),
    'a new baby takes up all the room': (0.533, 0.553, 0.530, 0.552, 0.496),
    'nobody watches the cartwheel': (0.551, 0.569, 0.547, 0.566, 0.515),
    'standing up for someone smaller': (0.615, 0.646, 0.593, 0.635, 0.612),
    'the glow of a gold star': (0.560, 0.567, 0.555, 0.559, 0.524),
    'a question that will not go to bed': (0.557, 0.603, 0.558, 0.582, 0.554),
    'an itch to build something': (0.548, 0.602, 0.551, 0.575, 0.546),
    'too much fizz to sit still': (0.537, 0.574, 0.540, 0.555, 0.535),
    'someone was kind when it counted': (0.609, 0.637, 0.585, 0.631, 0.616),
    'more stars than anyone could count': (0.584, 0.636, 0.578, 0.606, 0.581),
    'a test at school tomorrow': (0.639, 0.663, 0.598, 0.654, 0.627),
    'a stray dog follows you home': (0.545, 0.564, 0.536, 0.542, 0.529),
    'starting school': (0.490, 0.524, 0.505, 0.496, 0.476),
    'a game of hide and seek': (0.562, 0.593, 0.562, 0.569, 0.546),
    'your little cousin comes to stay': (0.574, 0.614, 0.573, 0.597, 0.566),
    'the last slice of birthday cake': (0.527, 0.559, 0.520, 0.546, 0.524),
    'Saturday chores': (0.596, 0.632, 0.586, 0.618, 0.591),
    'a day at the beach': (0.523, 0.553, 0.531, 0.541, 0.511),
    'a board game night with the family': (0.597, 0.641, 0.593, 0.631, 0.587),
    'a holiday meal with the whole family': (0.537, 0.557, 0.529, 0.522, 0.511),
    'the empty house at the end of the street': (0.589, 0.612, 0.587, 0.610, 0.573),
    'your first pocket money': (0.499, 0.532, 0.524, 0.503, 0.480),
    'a thunderstorm at night': (0.492, 0.512, 0.491, 0.488, 0.480),
    'a box of craft things and a free hour': (0.524, 0.547, 0.519, 0.524, 0.520),
    'sharing a room with your sibling': (0.531, 0.541, 0.525, 0.525, 0.516),
    'your pet dies': (0.584, 0.621, 0.584, 0.611, 0.579),
    'a new kid joins your class': (0.594, 0.630, 0.582, 0.615, 0.586),
    'the school play': (0.590, 0.639, 0.595, 0.610, 0.585),
    'a long car journey': (0.522, 0.540, 0.519, 0.539, 0.514),
    'a jar of tadpoles': (0.538, 0.564, 0.537, 0.552, 0.519),
    'sports day': (0.593, 0.627, 0.587, 0.617, 0.578),
    'your parents split up': (0.707, 0.682, 0.583, 0.696, 0.644),
    'two houses from now on': (0.549, 0.593, 0.552, 0.580, 0.546),
    'the family moves to a new town': (0.704, 0.681, 0.592, 0.714, 0.651),
    'moving to a new town': (0.559, 0.584, 0.555, 0.575, 0.535),
    'a grandparent dies': (0.560, 0.605, 0.559, 0.574, 0.563),
    'a pet of your own': (0.583, 0.613, 0.567, 0.583, 0.562),
    'you are picked for something special': (0.615, 0.646, 0.589, 0.630, 0.610),
    'the night it goes too far': (0.731, 0.621, 0.446, 0.763, 0.617),
    'an offer from people who do not ask twice': (0.635, 0.610, 0.435, 0.920, 0.498, 0.000),
    'the man who hurt your family walks free': (0.794, 0.578, 0.532, 0.549, 0.524, 0.000),
    'the neighbour who wants your land': (0.869, 0.489, 0.359, 0.539, 0.570, 0.000),
    'a business partner about to ruin you': (0.608, 0.661, 0.484, 0.707, 0.593, 0.000),
    'a dare to steal from the shop': (0.691, 0.673, 0.595, 0.697, 0.663),
    'a bag you should not ask about': (0.726, 0.685, 0.566, 0.695, 0.647),
    'a stranger on the pavement who does not get up': (0.631, 0.638, 0.492, 0.769, 0.515),
    'selling a little weed for quick money': (0.618, 0.651, 0.520, 0.740, 0.527),
    "a friend's scam is paying well": (0.635, 0.668, 0.521, 0.668, 0.510),
    'a pub argument turns into a fight': (0.602, 0.588, 0.442, 0.708, 0.501),
    'fiddling the books at work': (0.591, 0.553, 0.440, 0.661, 0.514),
    "the neighbour's van across your drive": (0.681, 0.518, 0.397, 0.615, 0.512),
    'an insurance claim for more than you lost': (0.765, 0.478, 0.354, 0.512, 0.568),
    'the first night in a cell': (0.819, 0.531, 0.455, 0.569, 0.521),
    'a friend asks you for an alibi': (0.607, 0.603, 0.494, 0.665, 0.494),
    'learning to use a new phone': (0.822, 0.455, 0.359, 0.481, 0.565),
    'a fall at home': (0.761, 0.439, 0.362, 0.511, 0.596),
    'a scam phone call': (0.727, 0.445, 0.384, 0.523, 0.579),
    "a grandchild's visit": (0.926, 0.440, 0.353, 0.454, 0.597),
    'a birthday party in your honour': (0.721, 0.442, 0.359, 0.511, 0.550),
    'the doctor says to stop driving': (0.851, 0.496, 0.372, 0.499, 0.540),
    'a sunny day in the park': (0.727, 0.470, 0.360, 0.543, 0.606),
    'sorting out your will': (0.742, 0.462, 0.368, 0.473, 0.571),
    'a memorial service for a friend': (0.818, 0.439, 0.354, 0.460, 0.572),
    'your children want to decide for you': (0.824, 0.451, 0.367, 0.506, 0.622),
    "a seat on the residents' committee": (0.842, 0.461, 0.374, 0.507, 0.616),
    'you cannot remember a word': (0.775, 0.462, 0.352, 0.453, 0.605),
    'a new friend at the community centre': (0.827, 0.478, 0.362, 0.485, 0.599),
    'the house you grew up in is for sale': (0.853, 0.512, 0.381, 0.499, 0.525),
    'an old grudge resurfaces': (0.917, 0.489, 0.368, 0.530, 0.579),
    'a young neighbour needs help': (0.896, 0.455, 0.368, 0.473, 0.622),
    'a protest to save the local hospital': (0.980, 0.480, 0.379, 0.473, 0.631),
    'a quiet hour remembering': (0.742, 0.461, 0.363, 0.432, 0.612),
    'tending an allotment': (0.846, 0.448, 0.360, 0.458, 0.714),
    'a game of cards with old rivals': (0.900, 0.445, 0.365, 0.455, 0.547),
    'the first months of retirement': (0.755, 0.507, 0.375, 0.522, 0.542),
    'your partner dies': (0.810, 0.497, 0.382, 0.480, 0.616),
    'moving to a smaller home or into care': (0.875, 0.483, 0.371, 0.517, 0.621),
    'a late love': (0.840, 0.493, 0.381, 0.507, 0.605),
    "honoured for your life's work": (0.839, 0.485, 0.361, 0.476, 0.571),
    'facing the end': (0.879, 0.426, 0.359, 0.489, 0.661),
    'a game, a club or clothes not for you': (0.513, 0.514, 0.481, 0.566, 0.503),
    "girls' jobs and boys' jobs at home": (0.514, 0.551, 0.520, 0.531, 0.503),
    'told to act like a proper girl or boy': (0.645, 0.675, 0.553, 0.644, 0.613),
    'the uniform rule for girls and boys': (0.652, 0.640, 0.548, 0.609, 0.608),
    'the only one of your kind at work': (0.603, 0.496, 0.417, 0.590, 0.455),
    'who stays home with the baby': (0.615, 0.542, 0.417, 0.658, 0.491),
    'starting treatment to live as yourself': (0.624, 0.629, 0.418, 0.852, 0.614),
    'a child of your own, another way': (0.661, 0.676, 0.434, 0.661, 0.481, 0.000),
    'growing old without hiding again': (0.818, 0.435, 0.364, 0.501, 0.613),
    'a feeling for a friend that does not fit': (0.664, 0.683, 0.600, 0.666, 0.654),
    'the clothes and the name that do not fit': (0.676, 0.710, 0.557, 0.689, 0.659),
    'someone mocked for being different': (0.620, 0.552, 0.437, 0.636, 0.506),
    'your sibling brings home a same-sex partner': (0.722, 0.666, 0.574, 0.707, 0.632),
    'the feeling is not going to pass': (0.714, 0.671, 0.576, 0.711, 0.633),
    'the first person you tell': (0.652, 0.721, 0.534, 0.658, 0.566),
    'a love nobody can know about': (0.715, 0.673, 0.576, 0.711, 0.641),
    'telling the family who you are': (0.678, 0.640, 0.497, 0.732, 0.577),
    'everyone asks when you will settle down': (0.611, 0.789, 0.492, 0.604, 0.545),
    'asking to be called by another name': (0.712, 0.666, 0.591, 0.780, 0.613),
    'a friend comes out to you': (0.653, 0.535, 0.433, 0.589, 0.539),
    'a pride march comes down the high street': (0.677, 0.516, 0.410, 0.592, 0.515, 0.011),
    'the same week, over and over': (0.624, 0.489, 0.398, 0.617, 0.501),
    "a friend's good news stings": (0.723, 0.596, 0.503, 0.624, 0.578),
    'guilt that will not go away': (0.671, 0.670, 0.571, 0.698, 0.601),
    'shame after a public failure': (0.848, 0.587, 0.549, 0.595, 0.580),
    'the itch to be somewhere else': (0.626, 0.516, 0.407, 0.587, 0.490),
    'the anniversary of a death': (0.653, 0.486, 0.408, 0.559, 0.522),
    'homesick': (0.671, 0.679, 0.574, 0.578, 0.636),
    'anger that keeps building': (0.754, 0.688, 0.572, 0.742, 0.595),
    'a craving that keeps calling': (0.418, 0.395, 0.336, 1.186, 0.459),
    'trapped by a promise': (0.734, 0.649, 0.427, 0.561, 0.543),
    'jealousy in love': (0.619, 0.547, 0.440, 0.601, 0.498),
    'feeling invisible': (0.846, 0.500, 0.404, 0.451, 0.541),
    'a sense of injustice': (0.766, 0.551, 0.428, 0.573, 0.512),
    'feeling old': (0.696, 0.442, 0.364, 0.574, 0.509),
    'wanting to be noticed': (0.847, 0.603, 0.507, 0.578, 0.558),
    'longing for a child': (0.774, 0.600, 0.495, 0.551, 0.509),
    'longing for love': (0.957, 0.559, 0.443, 0.500, 0.562),
    'the urge to protect': (0.681, 0.469, 0.366, 0.551, 0.513),
    'needing to be alone': (0.713, 0.678, 0.504, 0.615, 0.574),
    'pride after a success': (0.687, 0.618, 0.521, 0.647, 0.551),
    'a curiosity that will not let go': (0.678, 0.547, 0.421, 0.532, 0.565),
    'ambition wakes up': (0.688, 0.616, 0.446, 0.570, 0.480),
    'the urge to make something': (0.663, 0.530, 0.397, 0.571, 0.530),
    'a burst of energy': (0.573, 0.540, 0.448, 0.755, 0.502),
    'gratitude': (0.645, 0.456, 0.353, 0.506, 0.529),
    'a quiet contentment': (0.751, 0.442, 0.359, 0.424, 0.523),
    'hope after a hard time': (0.757, 0.587, 0.448, 0.584, 0.490),
    'inspiration strikes': (0.711, 0.532, 0.406, 0.635, 0.534),
    'awe': (0.663, 0.555, 0.420, 0.544, 0.537),
    'an old song brings it all back': (0.835, 0.453, 0.361, 0.428, 0.553),
    'someone asks you home after the party': (0.625, 0.595, 0.505, 0.701, 0.518),
    'a match who wants to meet tonight': (0.698, 0.486, 0.396, 0.551, 0.519),
    'your ex wants to try again': (0.616, 0.605, 0.508, 0.705, 0.514, 0.032),
    'a friend says they are in love with you': (0.651, 0.598, 0.512, 0.708, 0.534, 0.036),
    'single by choice, and everyone asks why': (0.732, 0.476, 0.396, 0.531, 0.529),
    'your partner asks to open the relationship': (0.687, 0.577, 0.467, 0.710, 0.507),
    'the last night of a work trip': (0.634, 0.526, 0.423, 0.651, 0.482),
    'years together, and the bedroom has gone quiet': (0.679, 0.509, 0.379, 0.573, 0.525),
    'desire and a body that is changing': (0.648, 0.495, 0.375, 0.548, 0.516),
    'a late passion': (0.592, 0.490, 0.368, 0.557, 0.495),
    'an invitation for three': (0.650, 0.652, 0.507, 0.730, 0.510),
    'a holiday romance': (0.695, 0.555, 0.459, 0.628, 0.549),
    'exams are coming': (0.716, 0.673, 0.587, 0.715, 0.644),
    'a fight after school': (0.700, 0.681, 0.593, 0.682, 0.655),
    'you learn a secret about a friend': (0.706, 0.680, 0.590, 0.713, 0.642),
    'summer camp': (0.704, 0.680, 0.593, 0.677, 0.653),
    'a party at a house with no parents': (0.722, 0.665, 0.575, 0.714, 0.643),
    'a Saturday job at the corner shop': (0.677, 0.679, 0.597, 0.677, 0.657),
    'a band or a sport that takes over your life': (0.692, 0.684, 0.595, 0.692, 0.649),
    'a group project where nobody pulls their weight': (0.711, 0.677, 0.585, 0.709, 0.653),
    'a coming-of-age ceremony': (0.657, 0.702, 0.603, 0.674, 0.646),
    'someone starts mocking you online': (0.703, 0.694, 0.603, 0.701, 0.661),
    'a teacher offers you a role of responsibility': (0.709, 0.680, 0.596, 0.678, 0.643),
    'a sleepless night wondering who you are': (0.710, 0.675, 0.576, 0.710, 0.637),
    'a new hobby you cannot put down': (0.698, 0.674, 0.592, 0.705, 0.644),
    'your sibling is in trouble and you know why': (0.687, 0.670, 0.600, 0.682, 0.644),
    'your body is changing': (0.649, 0.683, 0.596, 0.658, 0.657),
    'a debate or contest at school': (0.704, 0.692, 0.590, 0.688, 0.659),
    'a friend is being picked on': (0.704, 0.688, 0.600, 0.692, 0.662),
    'you are grounded for a week': (0.691, 0.680, 0.582, 0.696, 0.643),
    'a long walk alone': (0.693, 0.682, 0.563, 0.702, 0.652),
    'tryouts for the team': (0.700, 0.686, 0.583, 0.697, 0.649),
    'your first real job': (0.713, 0.670, 0.576, 0.720, 0.636),
    'a close friend moves away': (0.752, 0.681, 0.563, 0.721, 0.625),
    'money runs out at home': (0.746, 0.660, 0.579, 0.721, 0.623),
    'you win a scholarship or a place': (0.737, 0.668, 0.580, 0.724, 0.639),
    'a trip far from home': (0.720, 0.678, 0.571, 0.721, 0.617),
    'a teacher or coach who believes in you': (0.692, 0.676, 0.573, 0.739, 0.620),
    'a teacher who sees something in you': (0.610, 0.648, 0.606, 0.631, 0.605),
    'falling in love': (0.675, 0.651, 0.538, 0.748, 0.542),
    'making peace with family you had cut off': (0.734, 0.510, 0.418, 0.635, 0.574),
    'a parent dies': (0.634, 0.530, 0.429, 0.647, 0.517),
    'losing a parent too soon': (0.563, 0.590, 0.569, 0.589, 0.561),
    'a brother or sister dies': (0.851, 0.498, 0.375, 0.533, 0.585),
    'you take in a child who needs a home': (0.721, 0.531, 0.448, 0.589, 0.571),
    "a partner's affair comes to light": (0.742, 0.561, 0.404, 0.729, 0.559),
    'betrayed by a friend or a business partner': (0.749, 0.587, 0.434, 0.789, 0.550),
    'a friend for life': (0.665, 0.588, 0.463, 0.632, 0.536),
    'a best friend of your own': (0.620, 0.660, 0.595, 0.624, 0.608),
    'a long-lost relative finds you': (0.707, 0.546, 0.382, 0.566, 0.543),
    'welcomed into a community': (0.709, 0.545, 0.417, 0.599, 0.522),
    'a club where you belong': (0.613, 0.662, 0.599, 0.641, 0.617),
    'a narrow escape': (0.652, 0.537, 0.428, 0.626, 0.523),
    'a close call on the road': (0.584, 0.609, 0.564, 0.599, 0.572),
    'robbed or attacked in the street': (0.774, 0.605, 0.467, 0.692, 0.586),
    "your child's big success": (0.678, 0.458, 0.360, 0.491, 0.535),
    'your closest friend dies': (0.778, 0.463, 0.365, 0.507, 0.618),
    'losing a grandparent': (0.651, 0.642, 0.534, 0.739, 0.548),
    'a breakthrough in your work': (0.697, 0.590, 0.449, 0.661, 0.554),
    'an operation gives something back': (0.723, 0.484, 0.383, 0.507, 0.584),
    'an operation that makes things better': (0.577, 0.619, 0.551, 0.603, 0.565),
    'earning a qualification': (0.677, 0.606, 0.505, 0.693, 0.557),
    'the badge you worked for': (0.640, 0.674, 0.615, 0.656, 0.641),
    'money worries end': (0.675, 0.513, 0.403, 0.560, 0.522),
    'a stranger saves you, or you save one': (0.698, 0.565, 0.423, 0.582, 0.550),
    'a stranger to the rescue': (0.600, 0.608, 0.616, 0.605, 0.601),
    'a cause you fought for wins': (0.771, 0.559, 0.449, 0.568, 0.603),
    'financial ruin': (0.744, 0.611, 0.413, 0.760, 0.534),
    'losing the home': (0.721, 0.606, 0.447, 0.747, 0.556),
    'war comes': (0.805, 0.506, 0.444, 0.640, 0.542),
    'a public scandal': (0.736, 0.599, 0.454, 0.608, 0.544),
    'a heart attack or stroke': (0.794, 0.466, 0.352, 0.549, 0.606),
    'living with a chronic illness': (0.752, 0.520, 0.402, 0.614, 0.557),
    'growing up with an illness': (0.577, 0.617, 0.578, 0.583, 0.561),
    'a long dark season': (0.716, 0.611, 0.491, 0.682, 0.583),
    'a sadness that will not lift': (0.633, 0.663, 0.620, 0.700, 0.612),
    'an addiction takes hold': (0.742, 0.675, 0.514, 0.782, 0.610),
    'a new job at last': (0.648, 0.565, 0.440, 0.674, 0.512),
    'a younger colleague needs a mentor': (0.681, 0.483, 0.345, 0.518, 0.501),
    'a warning from the doctor': (0.698, 0.515, 0.382, 0.580, 0.595),
    'someone tries to push you out at work': (0.697, 0.542, 0.368, 0.632, 0.554),
    'a party for twenty-five years in the job': (0.642, 0.447, 0.344, 0.546, 0.471),
    'a sudden urge to buy something big': (0.697, 0.479, 0.352, 0.575, 0.504),
    'a long-planned trip': (0.686, 0.505, 0.354, 0.502, 0.517),
    'dancing at a wedding': (0.639, 0.491, 0.344, 0.509, 0.490),
    'your pension statement arrives': (0.697, 0.494, 0.358, 0.602, 0.532),
    'the club or congregation asks you to lead': (0.740, 0.474, 0.363, 0.560, 0.521),
    'an old flame gets in touch': (0.691, 0.477, 0.368, 0.505, 0.542),
    'a dispute over an inheritance': (0.720, 0.521, 0.364, 0.602, 0.530),
    'a sleepless night: is this all there is?': (0.664, 0.503, 0.349, 0.554, 0.498),
    'you take up an instrument or a language': (0.750, 0.508, 0.344, 0.507, 0.588),
    'a teenager in your care breaks the rules': (0.733, 0.506, 0.356, 0.536, 0.540),
    "an old friend's funeral": (0.671, 0.469, 0.365, 0.512, 0.499),
    'your town faces a change you could fight': (0.844, 0.526, 0.358, 0.568, 0.593),
    'a friend asks you to stand up for them': (0.775, 0.499, 0.358, 0.628, 0.498),
    'an afternoon in the garden': (0.683, 0.471, 0.342, 0.496, 0.573),
    'a grown child in the family asks for advice': (0.722, 0.469, 0.359, 0.505, 0.512),
    'you are offered the top job': (0.713, 0.512, 0.360, 0.546, 0.527),
    'the children leave home': (0.725, 0.516, 0.370, 0.540, 0.532),
    'divorce after twenty years': (0.783, 0.536, 0.375, 0.592, 0.524),
    'your first grandchild': (0.725, 0.499, 0.381, 0.524, 0.544),
    'a frightening diagnosis': (0.858, 0.501, 0.394, 0.534, 0.604),
    'an unexpected legacy': (0.685, 0.493, 0.388, 0.522, 0.541),
    'a chance to change everything': (0.714, 0.531, 0.403, 0.605, 0.541),
    "a first fish on a grandparent's line": (0.623, 0.654, 0.593, 0.654, 0.609),
    'the garden bird count': (0.600, 0.631, 0.584, 0.617, 0.591),
    'a chess tournament in the school hall': (0.617, 0.659, 0.583, 0.625, 0.626),
    'practice before tea': (0.639, 0.667, 0.606, 0.665, 0.626),
    'fishing the canal with friends': (0.680, 0.697, 0.589, 0.683, 0.653),
    'a late raid with the online team': (0.713, 0.667, 0.579, 0.711, 0.619),
    'two nights camping with friends by a lake': (0.726, 0.663, 0.567, 0.705, 0.625),
    'the Tuesday pub quiz': (0.660, 0.612, 0.502, 0.665, 0.518),
    'a first half marathon': (0.650, 0.620, 0.519, 0.755, 0.524, 0.000),
    "a beginners' salsa class": (0.637, 0.615, 0.509, 0.790, 0.514),
    'dawn on the lake, alone with a rod': (0.598, 0.510, 0.411, 0.600, 0.497),
    'a dinner for twelve from an untried recipe': (0.606, 0.534, 0.412, 0.631, 0.493),
    'Saturday walks for the dog shelter': (0.568, 0.521, 0.421, 0.647, 0.459),
    'an away match in the rain': (0.728, 0.473, 0.345, 0.536, 0.516),
    'a chair rescued from a skip': (0.709, 0.538, 0.351, 0.497, 0.544),
    'the dawn swimmers at the cove': (0.697, 0.515, 0.334, 0.548, 0.543),
    'teaching a grandchild to fish': (0.799, 0.470, 0.343, 0.466, 0.558),
    'a rare bird at the marsh hide': (0.789, 0.472, 0.364, 0.509, 0.578),
    'the knitting circle at the library': (0.891, 0.439, 0.366, 0.463, 0.638),
    "the camera club's theme of the month": (0.854, 0.452, 0.362, 0.478, 0.633),
    'a vape passed round behind the sports hall': (0.693, 0.670, 0.582, 0.691, 0.637),
    'a drinking game round the kitchen table': (0.691, 0.662, 0.553, 0.739, 0.572),
    'a bag of pills in the party kitchen': (0.690, 0.678, 0.557, 0.719, 0.586),
    'a dare on the factory roof': (0.707, 0.673, 0.581, 0.730, 0.598),
    "a joint going round at a friend's": (0.688, 0.662, 0.554, 0.722, 0.591),
    'cocaine at the office party': (0.573, 0.553, 0.445, 0.692, 0.475),
    'a race to the rocks across the bay': (0.636, 0.556, 0.466, 0.680, 0.469),
    'a pill offered in the festival crowd': (0.601, 0.641, 0.485, 0.746, 0.500),
    'the last pitch as the weather turns': (0.598, 0.581, 0.450, 0.658, 0.492),
    'the car keys after a few drinks': (0.602, 0.549, 0.459, 0.673, 0.487),
    'a friend who will not wake up': (0.674, 0.665, 0.515, 0.736, 0.550),
    'the last week of the painkillers': (0.803, 0.541, 0.424, 0.553, 0.573),
    'a racing heart after a heavy weekend': (0.667, 0.458, 0.408, 0.836, 0.654),
    'the cyclist at dusk': (0.838, 0.460, 0.387, 0.512, 0.621),
    'up the ladder to clear the gutters': (0.716, 0.457, 0.377, 0.494, 0.562),
    'the last afternoon of primary school': (0.644, 0.672, 0.612, 0.635, 0.642),
    'the first morning at the big school': (0.647, 0.682, 0.606, 0.670, 0.648),
    'nobody at the new school knows who you were': (0.648, 0.680, 0.615, 0.669, 0.654, 0.000),
    'a friend whose family lives on the river': (0.653, 0.690, 0.607, 0.666, 0.662),
    'the first Saturday in town without a grown-up': (0.648, 0.692, 0.604, 0.674, 0.645),
    'the table where you sit now': (0.660, 0.684, 0.614, 0.660, 0.662),
    'pens down on the last exam': (0.722, 0.658, 0.553, 0.728, 0.599),
    'the morning you leave home': (0.701, 0.646, 0.566, 0.730, 0.599),
    'work and a room abroad, if you go this month': (0.707, 0.663, 0.537, 0.768, 0.628, 0.000),
    'an apprenticeship that starts on Monday': (0.703, 0.680, 0.548, 0.704, 0.575, 0.000),
    'the first payslip and the first rent': (0.714, 0.648, 0.576, 0.724, 0.592),
    'the first weekend back, and the town looks smaller': (0.702, 0.676, 0.558, 0.724, 0.605),
    'the birthday party that ends at eleven': (0.589, 0.603, 0.481, 0.707, 0.491),
    'a contract with no end date': (0.626, 0.655, 0.481, 0.673, 0.467),
    'a training place in another line of work': (0.427, 0.601, 0.269, 0.690, 0.367, 0.001),
    'the ring in the drawer since spring': (0.633, 0.610, 0.485, 0.739, 0.500, 0.000),
    'a week with a shape of your own': (0.591, 0.630, 0.467, 0.723, 0.508, 0.000),
    'your parents at your table': (0.632, 0.605, 0.493, 0.707, 0.493),
    'the morning you turn fifty': (0.560, 0.492, 0.396, 0.560, 0.475),
    'the last of the old generation is buried': (0.626, 0.477, 0.404, 0.629, 0.495),
    'three months of leave, if you ask by Friday': (0.597, 0.514, 0.428, 0.632, 0.492, 0.046),
    'a spare place on a silent retreat': (0.614, 0.527, 0.408, 0.592, 0.509, 0.002),
    'the spare keys of half the family': (0.587, 0.490, 0.404, 0.591, 0.494),
    'a Saturday run in the park': (0.569, 0.542, 0.424, 0.645, 0.452),
    'the last day at work': (0.671, 0.454, 0.345, 0.479, 0.519),
    'the bus pass comes in the post': (0.770, 0.454, 0.344, 0.509, 0.496, 0.000),
    'a flat in the sun near old friends': (0.643, 0.483, 0.372, 0.495, 0.538, 0.000),
    'the college asks you to teach your trade': (0.796, 0.525, 0.370, 0.539, 0.533, 0.015),
    "a seat at the regulars' table": (0.660, 0.460, 0.331, 0.510, 0.514),
    'the pill box with seven little doors': (0.730, 0.484, 0.347, 0.491, 0.512, 0.002),
    'the promise at the first camp': (0.632, 0.664, 0.596, 0.639, 0.628),
    'the patrol chooses a new leader': (0.675, 0.675, 0.603, 0.664, 0.666),
    'the oldest one at the campfire': (0.721, 0.645, 0.583, 0.673, 0.664),
    'the first match in the club shirt': (0.630, 0.649, 0.583, 0.689, 0.656),
    'the coach asks who wants the armband': (0.664, 0.659, 0.592, 0.708, 0.672, 0.000),
    'one more season, or the last': (0.565, 0.561, 0.509, 0.795, 0.572, 0.000),
    'a customer shouts at the new face behind the till': (0.611, 0.569, 0.461, 0.755, 0.566),
    'the keys and the alarm code': (0.577, 0.538, 0.427, 0.739, 0.547, 0.022),
    'the owner wants to retire': (0.539, 0.460, 0.355, 0.744, 0.575, 0.003),
    'the first Friday night on the floor': (0.553, 0.559, 0.524, 0.814, 0.485),
    'a place behind the bar': (0.547, 0.528, 0.535, 0.801, 0.470, 0.010),
    'twenty holidays on the floor': (0.489, 0.466, 0.461, 0.759, 0.456),
    'the spreadsheet the last clerk left behind': (0.663, 0.565, 0.433, 0.621, 0.507),
    'the firm will pay for one course': (0.682, 0.577, 0.421, 0.583, 0.500, 0.029),
    'the one who knows where everything is': (0.564, 0.539, 0.401, 0.595, 0.517),
    'the first visit on the round alone': (1.142, 0.448, 0.398, 0.466, 0.477),
    'the nursing course the agency will half pay for': (1.075, 0.438, 0.390, 0.467, 0.462, 0.072),
    'the first client moves into a home': (1.042, 0.457, 0.467, 0.561, 0.523, 0.107),
    'week six of basic training': (0.699, 0.592, 0.528, 0.741, 0.551),
    'the papers to sign on again': (0.653, 0.606, 0.507, 0.784, 0.526, 0.000),
    'a section of nineteen-year-olds': (0.664, 0.531, 0.474, 0.751, 0.517, 0.011),
    'the back row on the first Monday': (1.284, 0.409, 0.406, 0.479, 0.391),
    'the head of year post is advertised': (1.279, 0.398, 0.376, 0.486, 0.400, 0.000),
    'nobody wrote down how it is really done': (0.608, 0.553, 0.440, 0.619, 0.480),
    'the first mistake with everyone watching': (0.641, 0.555, 0.444, 0.603, 0.476),
    'the job could grow in two directions': (0.573, 0.578, 0.435, 0.616, 0.495, 0.028),
    'the colleague who started the same month': (0.623, 0.570, 0.438, 0.670, 0.481),
    'the newcomers do it a new way': (0.588, 0.528, 0.411, 0.584, 0.502),
    'the biggest job of a career, late in the day': (0.626, 0.484, 0.409, 0.591, 0.467),
    'the pecking order nobody mentions': (0.685, 0.541, 0.437, 0.624, 0.543),
    'the first time the group counts on you': (0.667, 0.555, 0.432, 0.633, 0.549),
    'the job in the group nobody else wants': (0.702, 0.565, 0.453, 0.592, 0.556),
    'a newcomer gets the place you were waiting for': (0.684, 0.563, 0.451, 0.641, 0.545),
    'the newer members want to change how it is done': (0.691, 0.518, 0.426, 0.556, 0.560),
    'someone has to carry it on after you': (0.671, 0.499, 0.398, 0.557, 0.519),
    'the words everyone else already knows': (0.651, 0.564, 0.363, 0.523, 0.506),
    'a welcome that feels too warm': (0.671, 0.555, 0.363, 0.552, 0.509),
    'the keys to the meeting hall': (0.686, 0.555, 0.374, 0.519, 0.532),
    'when believing goes quiet for a while': (0.680, 0.573, 0.367, 0.579, 0.525, 0.002),
    'new voices at the old gatherings': (0.721, 0.572, 0.412, 0.556, 0.527),
    'the one they ring at night': (0.733, 0.551, 0.416, 0.615, 0.533),
    'the first argument that really matters': (0.640, 0.558, 0.449, 0.665, 0.506),
    'the first thing that is only theirs': (0.645, 0.563, 0.440, 0.642, 0.516),
    'a big offer in another city': (0.640, 0.606, 0.442, 0.640, 0.528),
    'talking only about the shopping list': (0.633, 0.567, 0.451, 0.658, 0.526, 0.004),
    'a new chapter proposed over breakfast': (0.629, 0.529, 0.383, 0.538, 0.515),
    'asked how the two of them have lasted': (0.617, 0.491, 0.380, 0.563, 0.488),
    'the first night alone in charge': (0.611, 0.588, 0.470, 0.678, 0.499),
    'advice from every side': (0.614, 0.590, 0.465, 0.706, 0.490),
    'a week with no room left in it': (0.600, 0.575, 0.450, 0.632, 0.493, 0.000),
    "the child's new favourite grown-up": (0.594, 0.570, 0.448, 0.704, 0.483),
    'needed a little less each year': (0.600, 0.515, 0.412, 0.622, 0.483, 0.000),
    'the young parents ask the old hand': (0.600, 0.505, 0.421, 0.592, 0.482),
    'a culture that smells wrong at closing time': (0.724, 0.505, 0.405, 0.434, 0.514),
    'the same two hundred samples a day': (0.662, 0.558, 0.456, 0.456, 0.549),
    'the cleanest sentence in the manuscript': (0.762, 0.551, 0.396, 0.658, 0.469),
    'three books due in the same fortnight': (0.590, 0.530, 0.366, 0.999, 0.881),
    'the last two people in the building': (0.894, 0.458, 0.427, 0.499, 0.435),
    'a client asks to cut out the agency': (1.067, 0.433, 0.419, 0.454, 0.466),
    'the gate where nobody waits': (0.647, 0.544, 0.459, 0.586, 0.626),
    'the round is redrawn': (0.665, 0.524, 0.447, 0.657, 0.557),
    'a sketch that matters more than it looks': (0.944, 0.554, 0.509, 0.539, 0.827),
    'a royalty statement smaller than the rent': (1.011, 0.378, 0.380, 0.463, 0.490),
    'a short answer with two meanings': (0.393, 0.463, 0.348, 0.731, 0.667),
    'the court work goes to an agency': (0.387, 0.501, 0.396, 1.202, 0.389),
    'a hard companion in the quiet life': (1.227, 0.342, 0.367, 0.382, 0.441),
    "the community's guesthouse needs a manager": (1.091, 0.393, 0.380, 0.422, 0.482),
    'the old harvest song in a hard year': (0.534, 0.734, 0.363, 0.679, 0.469),
    'a gifted newcomer at the keyboard': (0.568, 0.688, 0.361, 0.655, 0.450),
    'defending a speaker you cannot stand': (0.662, 0.617, 0.395, 0.640, 0.612),
    "a seat on the council's camera panel": (0.769, 0.616, 0.429, 0.670, 0.584),
    'the free app the volunteers want': (0.635, 0.792, 0.433, 0.471, 0.495),
    "the town website's keeper wants out": (0.626, 0.749, 0.423, 0.541, 0.541),
    'an open rehearsal at the community choir': (0.405, 0.561, 0.223, 0.604, 0.256, 0.000),
    'a band that needs a drummer': (0.611, 0.326, 0.435, 0.217, 0.497, 0.001),
    'a broken lamp at the repair cafe': (0.385, 0.548, 0.439, 0.666, 0.297, 0.004),
    'a community kitchen short of hands': (0.630, 0.566, 0.229, 0.485, 0.380, 0.004),
    'a recruitment evening for the rescue team': (0.457, 0.531, 0.477, 0.518, 0.498, 0.000),
    'the lifeboat station calls for crew': (0.584, 0.561, 0.250, 0.650, 0.413, 0.000),
    'a vacancy for a parent governor': (0.555, 0.423, 0.363, 0.538, 0.394, 0.000),
    "the parents ask you to run the year's events": (0.550, 0.513, 0.408, 0.617, 0.424, 0.000),
    'the congregation needs someone to teach the class': (0.584, 0.333, 0.400, 0.389, 0.533, 0.005),
    'an invitation to a dialogue circle': (0.606, 0.530, 0.394, 0.607, 0.521, 0.000),
    'a faith that answers back': (0.452, 0.689, 0.338, 0.523, 0.532, 0.000),
    'a teacher with all the answers': (0.462, 0.611, 0.324, 0.649, 0.502),
    'the help that now feels like hovering': (0.817, 0.368, 0.346, 0.416, 0.633),
    'a week off from caring': (0.947, 0.380, 0.355, 0.447, 0.580),
    'a form with no box for the two of you': (0.664, 0.468, 0.371, 0.484, 0.592),
    'your life partner falls for someone': (0.732, 0.517, 0.392, 0.477, 0.568),
    'advice on the tip of the tongue': (0.762, 0.452, 0.349, 0.467, 0.577),
    'a grown child asks for a loan': (0.784, 0.505, 0.358, 0.525, 0.597),
    'the school gate a generation on': (0.730, 0.438, 0.350, 0.531, 0.587, 0.000),
    "a call from the grandchild's parent": (0.791, 0.442, 0.343, 0.601, 0.525),
    'the new voice that rushes the phrase': (0.700, 0.451, 0.417, 0.432, 0.814),
    'a solo at the spring concert': (0.747, 0.449, 0.474, 0.449, 0.681),
    'whose history the show leaves out': (0.741, 0.434, 0.583, 0.419, 0.577),
    'the encampment in the rain': (0.605, 0.398, 0.505, 0.498, 0.468),
    'a story nobody in town has covered': (0.970, 0.461, 0.388, 0.404, 0.651),
    'a guest who does not turn up': (0.873, 0.453, 0.349, 0.388, 0.565),
    'a roof three households cannot pay for': (0.697, 0.794, 0.391, 0.454, 0.537),
    'an empty flat in the cooperative': (0.663, 0.792, 0.389, 0.479, 0.534),
    'a veteran and a newcomer at one table': (0.613, 0.743, 0.341, 0.468, 0.411),
    'the café wants rent for the back room': (0.736, 0.760, 0.364, 0.508, 0.449),
    'your partner falls seriously ill': (0.724, 0.496, 0.383, 0.571, 0.571, 0.009),
    'going into foster care': (0.517, 0.552, 0.508, 0.539, 0.501),
    'election day': (0.661, 0.533, 0.399, 0.597, 0.511),
    'a petition comes round': (0.634, 0.531, 0.426, 0.572, 0.536),
    'a strike vote at work': (0.672, 0.539, 0.453, 0.636, 0.518),
    'a march on a working day': (0.618, 0.503, 0.418, 0.654, 0.505),
    'the call to serve': (0.771, 0.678, 0.549, 0.643, 0.552, 0.012),
    'a landslide on election night': (0.692, 0.522, 0.400, 0.598, 0.545),
    'the old order falls': (0.729, 0.609, 0.431, 0.649, 0.544),
    'a revival fills the square': (0.700, 0.548, 0.420, 0.647, 0.543, 0.000),
    'a cure is found at last': (0.716, 0.527, 0.393, 0.601, 0.570),
    'everyone is suddenly on the new medium': (0.706, 0.572, 0.482, 0.625, 0.560),
    'the machines come for the work': (0.673, 0.574, 0.459, 0.664, 0.542, 0.001),
    'the power and the networks go down': (0.684, 0.571, 0.441, 0.613, 0.559),
    'a crash takes the savings': (0.685, 0.534, 0.450, 0.593, 0.545),
    'a parent who longs for a grandchild': (0.607, 0.596, 0.494, 0.754, 0.530),
    'a parent asks you to take over the family shop': (0.684, 0.707, 0.556, 0.700, 0.518, 0.006),
    'a parent who can no longer live alone': (0.682, 0.501, 0.384, 0.607, 0.510, 0.020),
    'a parent asks you to move back home': (0.640, 0.520, 0.410, 0.613, 0.508),
    'a brother or sister in debt asks for help': (0.652, 0.546, 0.429, 0.617, 0.525),
    'a colleague after your job': (0.665, 0.568, 0.445, 0.693, 0.531),
    'a weekend away, if you say yes': (0.640, 0.559, 0.471, 0.685, 0.517),
    'a letter from the friend you cut off': (0.708, 0.548, 0.437, 0.588, 0.512),
    'an intervention at the kitchen table': (0.679, 0.585, 0.429, 0.680, 0.502),
    'a secret a parent has kept for forty years': (0.559, 0.572, 0.443, 0.813, 0.496),
    'the first months in a new country': (0.535, 0.510, 0.469, 0.594, 0.627),
    'learning the local language': (0.546, 0.525, 0.492, 0.605, 0.666),
    'residence papers at the government office': (0.569, 0.539, 0.477, 0.687, 0.653),
    'the oath of citizenship': (0.548, 0.526, 0.453, 0.587, 0.604, 0.000),
    'a deadline at college or work': (0.689, 0.663, 0.529, 0.725, 0.539),
    'a night out that gets out of hand': (0.661, 0.626, 0.522, 0.733, 0.529),
    'a flatmate who does not pay their share': (0.684, 0.660, 0.537, 0.733, 0.565),
    "a friend's wedding": (0.712, 0.657, 0.565, 0.726, 0.597),
    'a dating app match': (0.652, 0.638, 0.570, 0.771, 0.566),
    'learning to cook for yourself': (0.693, 0.644, 0.551, 0.737, 0.579),
    'a festival weekend': (0.626, 0.624, 0.545, 0.726, 0.533),
    'your first tax form and a stack of bills': (0.715, 0.666, 0.567, 0.742, 0.619),
    'your parents expect you home for the holidays': (0.649, 0.632, 0.545, 0.764, 0.539),
    'an idea for a side business': (0.693, 0.667, 0.544, 0.786, 0.547),
    'a job interview': (0.705, 0.663, 0.532, 0.774, 0.545),
    'awake at night worrying about the future': (0.620, 0.647, 0.522, 0.747, 0.535),
    'a heated argument online about politics': (0.726, 0.676, 0.531, 0.807, 0.541),
    'a friend asks to borrow money': (0.673, 0.654, 0.526, 0.730, 0.553),
    "a colleague's mistake you could use": (0.648, 0.639, 0.526, 0.735, 0.553),
    'a volunteer drive in your neighbourhood': (0.646, 0.661, 0.507, 0.731, 0.529),
    'a protest in your city': (0.648, 0.676, 0.541, 0.760, 0.540),
    'flu, alone in a rented room': (0.667, 0.667, 0.519, 0.764, 0.538),
    'a weekend hike': (0.615, 0.634, 0.518, 0.776, 0.529),
    'a promotion is open': (0.694, 0.693, 0.547, 0.780, 0.547),
    'moving in with a partner': (0.621, 0.623, 0.477, 0.710, 0.510),
    'a breakup': (0.630, 0.631, 0.502, 0.707, 0.513),
    'your first full-time job': (0.631, 0.642, 0.517, 0.735, 0.516),
    'losing your job': (0.695, 0.600, 0.469, 0.695, 0.541),
    'a baby on the way, planned or not': (0.645, 0.626, 0.486, 0.717, 0.511),
    'an unexpected chance: a grant, a role, a stage': (0.621, 0.562, 0.455, 0.665, 0.539),
    'the police at the door': (0.956, 0.565, 0.474, 0.506, 0.497),
    'a promise you broke comes back': (0.604, 0.594, 0.470, 0.709, 0.526),
    'a promise kept for years pays off': (0.682, 0.520, 0.402, 0.530, 0.494),
    'someone you helped returns the favour': (0.638, 0.526, 0.409, 0.555, 0.520),
    'the one you turned away is the one who can help': (0.623, 0.523, 0.483, 0.619, 0.589),
    'an old enemy holds the keys': (0.702, 0.546, 0.432, 0.656, 0.509),
    'an old friend turns up when you need one': (0.641, 0.511, 0.399, 0.564, 0.516),
    'the office you defied remembers': (0.651, 0.555, 0.457, 0.863, 0.602),
    'they ask you to lead because you stood up once': (0.621, 0.530, 0.455, 0.755, 0.579),
    'the same pressure, again': (0.834, 0.518, 0.446, 0.510, 0.629),
    'you catch someone doing what you once did': (0.629, 0.587, 0.459, 0.629, 0.527),
    'years of practice are noticed': (0.660, 0.545, 0.423, 0.571, 0.539),
    'a gamble that paid asks for another': (0.605, 0.555, 0.446, 0.834, 0.553),
    'the body remembers the wild years': (0.578, 0.497, 0.413, 0.694, 0.516),
    'the home you left has changed': (0.610, 0.466, 0.595, 0.574, 0.526),
    'the place you stayed needs you now': (1.042, 0.542, 0.311, 0.380, 0.493),
    'roots call the one who moved away': (0.525, 0.550, 0.407, 0.717, 0.464),
    'the same chance comes round again': (0.673, 0.493, 0.399, 0.536, 0.602),
    'you never learned to swim': (0.676, 0.563, 0.403, 0.622, 0.498),
    'the apology that was never made': (0.480, 0.776, 0.480, 0.375, 0.768),
    'words that were never said': (0.682, 0.477, 0.395, 0.614, 0.494),
    'twenty-five years together': (0.675, 0.454, 0.361, 0.522, 0.490),
    'among the faith you left': (0.592, 0.549, 0.439, 0.699, 0.481),
    "your words in your child's mouth": (0.615, 0.471, 0.350, 0.502, 0.506),
    'someone faces what you came through': (0.654, 0.523, 0.389, 0.565, 0.499),
    'lean times, again': (0.629, 0.490, 0.379, 0.572, 0.507),
    'every hour belongs to someone else': (1.353, 0.364, 0.335, 0.356, 0.442),
    'the notebooks come together': (0.430, 1.367, 0.363, 0.374, 0.433),
    'a cushion of your own': (0.464, 0.406, 1.303, 0.380, 0.422),
    'all stories and no savings': (0.474, 0.380, 0.327, 1.300, 0.430),
    'everything rested on the one thing': (0.501, 0.377, 0.318, 0.352, 1.311),
    'waking up in hospital': (0.611, 0.523, 0.436, 0.880, 0.540),
    'volunteers wanted to count what lives here': (0.704, 0.512, 0.405, 0.540, 0.533, 0.059),
    'a project online asks for a thousand pairs of eyes': (0.628, 0.537, 0.410, 0.615, 0.506, 0.040),
    'a lab needs hands for the summer': (0.715, 0.707, 0.475, 0.771, 0.486, 0.432),
    'a research post you are half qualified for': (0.655, 0.575, 0.484, 0.716, 0.448, 0.330),
    'the contract runs out': (0.738, 0.501, 0.468, 0.604, 0.388, 0.137),
    'a fellowship of your own': (0.590, 0.717, 0.368, 0.786, 0.425, 0.294),
    'leaving research for another life': (0.564, 0.772, 0.413, 0.589, 0.432, 0.110),
    'the funding call closes on Friday': (0.814, 0.549, 0.459, 0.768, 0.476),
    'pressure to say more than the data show': (0.657, 0.591, 0.397, 0.597, 0.563),
    'an error in your published work': (0.645, 0.644, 0.402, 0.527, 0.461),
    'the field season is lost': (0.771, 0.490, 0.384, 0.841, 0.467),
    'an old dataset suddenly matters': (0.882, 0.613, 0.421, 0.585, 0.477),
    'a community proposes a better question': (0.830, 0.468, 0.375, 0.543, 0.517, 0.250),
    'whose name goes first': (0.599, 0.606, 0.410, 0.600, 0.421),
    'a collaboration that goes unusually well': (0.909, 0.397, 0.415, 0.746, 0.446),
    'a finding that makes the news': (0.752, 0.662, 0.415, 0.550, 0.502),
    "a rival's result contradicts yours": (0.788, 0.762, 0.392, 0.516, 0.432),
    'the survey wants a paid assistant': (0.763, 0.431, 0.706, 0.375, 0.747, 0.375),
    'the code everyone uses has a bug': (0.396, 1.266, 0.422, 0.382, 0.384),
    'a paper that thanks everyone but your software': (0.430, 1.211, 0.437, 0.397, 0.381, 0.148),
    'a request for data you promised to protect': (0.393, 1.097, 0.351, 0.454, 0.428),
    'the archive nobody funds': (0.417, 1.222, 0.357, 0.410, 0.438),
    'the evidence points where nobody wants it to': (0.591, 0.743, 0.323, 0.383, 0.554),
    'a hundred studies and no agreement': (0.490, 0.996, 0.333, 0.391, 0.599),
    'the headline gets it wrong': (1.002, 0.373, 0.315, 0.638, 0.367),
    'a live interview on a hard question': (0.646, 0.383, 0.315, 0.897, 0.376),
    'the meeting in the village hall': (1.391, 0.379, 0.344, 0.403, 0.434),
    'whose data are these': (1.383, 0.406, 0.371, 0.340, 0.467),
    'the same stretch of river, every Sunday': (0.807, 0.497, 0.364, 0.457, 0.520),
    'your record does not match the official one': (0.825, 0.533, 0.362, 0.498, 0.534),
    'forty years of rain in one notebook': (0.880, 0.363, 0.408, 0.363, 0.547),
    'the developers want your survey': (0.759, 0.392, 0.446, 0.381, 0.712),
    'volunteers drifting away': (0.690, 0.520, 0.362, 0.451, 0.529),
    "a scientist wants your volunteers' data": (0.783, 0.463, 0.386, 0.475, 0.480),
    'the protocol says one thing, the supervisor another': (0.650, 0.511, 0.495, 0.578, 0.412),
    'your name is not on the paper': (0.651, 0.621, 0.509, 0.737, 0.425, 0.243),
    'a careful result that says no': (0.547, 0.722, 0.414, 0.594, 0.400, 0.063),
    'the reviewers come back': (0.666, 0.665, 0.401, 0.554, 0.416),
    'the budget will not stretch to everything': (0.625, 0.584, 0.424, 0.647, 0.435, 0.393),
    'a team member knows more than you now': (0.660, 0.609, 0.373, 0.539, 0.403),
    'eight people and one grant': (0.913, 0.516, 0.368, 0.623, 0.631),
    'the old instrument fails before the big run': (0.674, 0.492, 0.427, 0.545, 0.566),
    'every group wants the machine first': (0.678, 0.498, 0.489, 0.580, 0.491),
    'the first week with your own bench': (0.571, 0.597, 0.395, 0.592, 0.406, 0.055),
    'the experiment that will define you': (0.663, 0.655, 0.414, 0.614, 0.413),
    'half a year in, the work has a shape': (0.588, 0.606, 0.399, 0.584, 0.412),
    'hiring the first two people': (0.794, 0.583, 0.359, 0.662, 0.617),
    'the culture you set now': (0.788, 0.587, 0.355, 0.657, 0.625),
    'nobody to report to on Monday': (0.667, 0.380, 0.351, 1.121, 0.403),
    'the silence after the first rejection': (0.662, 0.385, 0.349, 1.120, 0.405),
    "a rhythm of one's own": (0.670, 0.386, 0.354, 1.110, 0.404),
    'your name on the door of the machine room': (0.724, 0.588, 0.439, 0.779, 0.439),
    'what the facility is for': (0.736, 0.638, 0.564, 0.614, 0.432),
    "the users' meeting goes quietly": (0.648, 0.749, 0.321, 0.846, 0.376),
    'the finding will not leave you alone': (0.557, 0.517, 0.416, 0.587, 0.517, 0.208),
    'a question from childhood comes back': (0.670, 0.487, 0.347, 0.547, 0.525, 0.063),
    'leaflets to deliver before Saturday': (0.709, 0.491, 0.400, 0.544, 0.512, 0.009),
    'poll workers wanted for election day': (0.623, 0.511, 0.404, 0.571, 0.517, 0.140),
    'the ward needs a candidate': (0.295, 0.358, 0.213, 0.501, 0.429, 0.333),
    'a paid job on the campaign': (0.779, 0.696, 0.348, 0.532, 0.554, 0.285),
    'polling day in the ward': (0.584, 0.107, -0.036, 0.293, 0.110, 0.018),
    'a seat falls vacant': (0.401, 0.300, 0.061, 0.461, 0.161, 0.265),
    'leaving politics for another life': (0.793, 0.355, 0.530, 0.747, 0.472, 0.131),
    'the hustings in the church hall': (0.903, 0.419, 0.351, 0.623, 0.464),
    'the money runs short three weeks out': (0.789, 0.465, 0.371, 0.665, 0.518),
    'a vote against your conscience': (0.742, 0.514, 0.340, 0.620, 0.490),
    'a deal to get it through': (0.830, 0.531, 0.344, 0.549, 0.468),
    'the constituency wants one thing, the party another': (0.808, 0.515, 0.358, 0.644, 0.523),
    'a run for mayor from outside the council': (0.880, 0.433, 0.401, 0.490, 0.460, 0.121),
    'polling day for mayor': (0.745, 0.588, 0.523, 0.603, 0.477, 0.227),
    'the campaign loses its organiser': (0.865, 0.529, 0.474, 0.635, 0.672, 0.280),
    'a family about to lose their home': (0.740, 0.689, 0.464, 0.566, 0.539),
    'the same case for the third time': (0.699, 0.882, 0.454, 0.531, 0.533),
    'the leadership wants its favourite selected': (0.629, 0.888, 0.479, 0.527, 0.539),
    'the party is broke after the election': (0.580, 0.903, 0.491, 0.555, 0.521),
    'a client wants the minister by Friday': (0.666, 0.839, 0.455, 0.477, 0.484),
    'an old colleague now decides': (0.594, 0.684, 0.520, 0.451, 0.460),
    'the report the funders will not like': (0.622, 0.822, 0.382, 0.437, 0.422),
    'a party takes your idea and twists it': (0.797, 0.744, 0.364, 0.492, 0.403),
    'the line the leader will not say': (0.441, 0.362, 0.315, 1.327, 0.293),
    'the speech is due at midnight': (0.448, 0.362, 0.308, 1.330, 0.288),
    'the poll that says your client is losing': (0.469, 1.353, 0.334, 0.320, 0.393),
    'the night the exit poll lands': (0.546, 1.324, 0.390, 0.370, 0.475),
    'a door slammed in your face': (0.924, 0.442, 0.370, 0.568, 0.515),
    'the candidate remembers your name': (0.761, 0.436, 0.366, 0.567, 0.573),
    'a voter not on the list': (0.659, 0.501, 0.410, 0.518, 0.535),
    'the count runs past midnight': (0.630, 0.449, 0.384, 0.538, 0.493),
    'the annual meeting nobody comes to': (0.614, 0.855, 0.383, 0.410, 0.532),
    'two members want the same nomination': (0.619, 0.821, 0.394, 0.404, 0.552),
    'forty volunteers and one weekend left': (0.700, 0.604, 0.486, 0.512, 0.652),
    'the candidate goes off script': (0.662, 0.624, 0.437, 0.413, 0.531),
    'news the boss does not want to hear': (0.852, 0.679, 0.417, 0.565, 0.556),
    'a briefing off the record': (0.750, 0.746, 0.410, 0.517, 0.573),
    'the bins have not been collected': (0.635, 0.480, 0.785, 0.657, 0.378),
    'the first full council meeting': (0.803, 0.536, 0.381, 0.721, 0.465),
    'the ward knows your name now': (0.809, 0.530, 0.391, 0.703, 0.483),
    'the chain of office': (0.691, 0.530, 0.502, 0.792, 0.376),
    'the day job or the town': (0.667, 0.599, 0.493, 0.756, 0.371),
    'the kind of mayor you will be': (0.680, 0.607, 0.494, 0.736, 0.370),
    'the first budget passes': (0.689, 0.605, 0.499, 0.735, 0.376),
    'the fight that made you want to stand': (0.636, 0.505, 0.418, 0.584, 0.550, 0.014),
    'a flyer for the youth theatre': (0.667, 0.667, 0.583, 0.663, 0.638, 0.004),
    'auditions for the school production': (0.672, 0.668, 0.603, 0.692, 0.642, 0.042),
    'the local players need a cast': (0.612, 0.531, 0.414, 0.596, 0.530, 0.298),
    'extras wanted for a film in town': (0.731, 0.588, 0.433, 0.598, 0.609, 0.238),
    'drama school auditions': (0.747, 0.649, 0.421, 0.771, 0.531, 0.190),
    'an open audition in the city': (0.684, 0.766, 0.499, 0.672, 0.612, 0.207),
    'the showcase for agents': (0.720, 0.702, 0.296, 0.498, 0.549, 0.346),
    'the part of a lifetime is cast': (0.906, 0.547, 0.437, 0.548, 0.654, 0.299),
    'opening night at the fringe': (0.644, 0.729, 0.393, 0.530, 0.813, 0.717),
    'casting night at the local players': (0.768, 0.694, 0.413, 0.563, 0.595, 0.633),
    'the summer show casts its lead': (0.709, 0.687, 0.591, 0.689, 0.635, 0.325),
    'a casting call for children': (0.641, 0.710, 0.630, 0.703, 0.662, -0.074),
    'a voice for the cartoon': (0.593, 1.071, 0.457, 0.668, 0.450, 0.324),
    'the stage management team is a person short': (0.655, 0.711, 0.463, 0.548, 0.613, 0.272),
    'a director is needed for the autumn play': (0.818, 0.740, 0.392, 0.610, 0.689, 0.645),
    'the script competition': (0.741, 0.863, 0.475, 0.593, 0.540, 0.416),
    'leaving acting for another life': (0.059, 0.593, -0.231, 0.685, 0.472, 0.221),
    "the city wants the town's show": (0.586, 1.028, 0.426, 0.480, 0.506, 0.442),
    'the lead is not in at the half': (0.418, 0.734, 0.398, 0.674, 0.458),
    'the fit-up runs through the night': (0.390, 0.869, 0.343, 0.542, 0.398),
    'the actor who cried in the waiting room': (0.862, 0.806, 0.731, 0.487, 0.801),
    'two clients, one part': (0.416, 0.939, 0.322, 0.859, 0.621),
    'the client who has not worked in a year': (0.448, 0.928, 0.340, 0.836, 0.609),
    'drama cut from the timetable': (0.491, 0.733, 0.376, 0.806, 0.450),
    'the shy child who wants a line': (0.401, 0.586, 0.358, 0.902, 0.429),
    'a year as the villain': (0.535, 1.073, 0.394, 0.451, 0.336),
    'the voice is going': (0.529, 1.169, 0.423, 0.433, 0.341),
    'closing on Saturday': (0.392, 1.267, 0.360, 0.151, 0.370),
    'an investor wants a part for a nephew': (0.620, 1.008, 0.391, 0.409, 0.382),
    'you, say this line': (0.728, 0.532, 0.379, 0.483, 0.491),
    'fourteen hours in a field for one shot': (0.721, 0.514, 0.363, 0.485, 0.484),
    'the oldest member wants the lead again': (0.529, 0.686, 0.367, 0.446, 0.465),
    'the pantomime that pays for the year': (0.557, 0.517, 0.351, 0.516, 0.487),
    'a safe season or the new writers': (0.360, 0.810, 0.331, 0.392, 0.622),
    'eight months on tour': (0.595, 0.614, 0.362, 0.725, 0.495),
    'a self-tape due by nine tomorrow': (0.602, 0.516, 0.367, 0.605, 0.537),
    'the producers want a star for the transfer': (0.676, 0.444, 0.666, 0.760, 0.363),
    'a cast member in trouble on the night': (0.529, 0.650, 0.355, 0.665, 0.383),
    'the understudy rehearsal nobody watches': (1.080, 0.392, 0.327, 0.495, 0.347),
    'the lead plays through a fever': (1.181, 0.515, 0.379, 0.491, 0.498),
    'the voice teacher and the accent from home': (0.717, 0.548, 0.394, 0.518, 0.469),
    'the money runs out in the second year': (0.904, 0.519, 0.410, 0.500, 0.394),
    'the lead does not believe in the idea': (0.351, 1.103, 0.316, 0.408, 0.527),
    'the budget is cut by a third': (0.370, 0.890, 0.306, 0.481, 0.590),
    'the producers want a different ending': (0.420, 0.970, 0.367, 0.586, 0.385),
    'the blank page at three in the morning': (0.498, 0.857, 0.664, 0.565, 0.438),
    'a newcomer gets your part': (0.598, 0.554, 0.415, 0.617, 0.560),
    'show week in the village hall': (0.643, 0.691, 0.384, 0.470, 0.507),
    'the new child gets the lead': (0.683, 0.668, 0.572, 0.698, 0.634),
    'first night nerves in the wings': (0.675, 0.671, 0.589, 0.682, 0.615),
    'the first morning of the first term': (0.536, 0.558, 0.421, 0.684, 0.461),
    'the movement class where you cannot hide': (0.602, 0.573, 0.438, 0.633, 0.500),
    'who you are when you are not acting': (0.623, 0.582, 0.456, 0.645, 0.508),
    'the first-year assessment': (0.574, 0.594, 0.423, 0.632, 0.504),
    'the first paid read-through': (0.520, 0.561, 0.374, 0.584, 0.436),
    'the second job does not come': (0.563, 0.615, 0.386, 0.586, 0.470),
    'what kind of actor you will be': (0.591, 0.620, 0.376, 0.713, 0.410),
    'half a year on, still an actor': (0.564, 0.587, 0.363, 0.583, 0.393),
    'the first day of rehearsals': (0.389, 1.279, 0.337, 0.464, 0.493),
    'the designer who wants a different show': (0.388, 1.276, 0.337, 0.459, 0.505),
    'the show you want to make': (0.386, 1.284, 0.337, 0.454, 0.506),
    'press night': (0.391, 1.279, 0.340, 0.453, 0.508),
    'the part you never got to play': (0.753, 0.720, 0.563, 0.589, 0.559, 0.141),
    'never too late for the stage': (0.693, 0.505, 0.378, 0.460, 0.559, 0.172),
    'the show you wrote to star in': (0.600, 0.637, 0.135, 0.701, 0.497),
    'reconsidering a commitment': (0.776, 0.568, 0.449, 0.653, 0.569),
}

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

# ---- content packs (chroma-packs/, the pathways and packs thread): the engine's conditions for each pack's echoes, inner and
# read moments (batch._packs merges them over INNER, ECHO, LIFE and READ). A season's moments (threshold:) need none.
_RESEARCH = ("has('research assistant') | has('research scientist') | has('research project lead') | "
             "has('research group leader') | has('research facility lead') | has('independent investigator') | "
             "has('research software engineer') | has('research data steward') | has('evidence synthesis specialist')")
PACK_RULES = {
    "science": dict(
        ECHO={
            # a breakthrough at work outside research that keeps asking to be understood (the applied translator's door)
            "the finding will not leave you alone": dict(
                anchor=f"had(['a breakthrough in your work'], {JUST})", req=f"~({_RESEARCH}) & (age >= 18)",
                more=["has('graduate')", "(hU + hR) > .5", "time > .5"],
                less=["stress > 1.5", "money < .2", "held_children & (kids_home > 0) & (time < .3)"]),
            # a child's wonder, back decades later with time to spare (the late entrant's door)
            "a question from childhood comes back": dict(
                anchor=f"had(['a curiosity that will not let go', 'awe'], {JUST}) & (age < 20)",
                req="(age >= 27) & (time > .4)",
                more=["retired", "~held_career", "kids_home == 0"],
                less=["stress > 1.5", "money < .2", "health < .3"]),
        },
        ROLES={
            # the catalogue has a professor on a research scientist or a group leader; the proposed rule named only the first
            "professor": dict(refines="research scientist; research group leader"),
        },
        READ={
            # a year's results come back null: only to someone with a research project under way
            "the results are in": dict(req="has('a research project under way')"),
        },
    ),
    "politics": dict(
        ECHO={   # the packs thread's proposal (chroma-packs/politics/engine-conditions.py, 22:56), taken as written
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
        },
    ),
}
# ---- pack conditions pasted from the packs' engine-conditions.py (calib_v7/paste_pack_rules.py; the engine may reword them here)
# part politics BASE ECHO
PACK_RULES.setdefault('politics', {}).setdefault('ECHO', {}).update({'the fight that made you want to stand': {'anchor': "had(['your town faces a change you could fight', 'a protest to "
                                                     "save the local hospital', 'a sense of injustice', 'a bitter "
                                                     "election', 'they ask you to lead because you stood up once'], "
                                                     '0.08333333333333333)',
                                           'req': "~(has('local councillor') | has('mayor') | has('member of "
                                                  "parliament')) & (age >= 18)",
                                           'more': ["has('activist in a cause')",
                                                    "has('party member')",
                                                    '(hW + hR) > .5'],
                                           'less': ['stress > 1.5', 'health < .3']},
 'the debate you never forgot': {'anchor': "had(['a debate or contest at school', 'defending a speaker you cannot "
                                           "stand'], 0.08333333333333333) & (age < 30)",
                                 'req': '(age >= 19) & (time > .4)',
                                 'more': ['retired', 'kids_home == 0', "has('public speaking')"],
                                 'less': ['stress > 1.5', 'money < .2']}})
# part politics LONGSHOTS ECHO
PACK_RULES.setdefault('politics', {}).setdefault('ECHO', {}).update({'the race comes round again': {'anchor': "has('a long shot that missed') & had(['election night', 'polling day for "
                                          "mayor', 'a challenge from the back benches', 'the campaign nobody gave a "
                                          "chance', 'the leadership falls vacant'], 0.08333333333333333) & "
                                          '(ago_fail_long < 0.08333333333333333)',
                                'req': "(age <= 80) & (health > .35) & (ago_fail_long >= sa) & (~had(['a challenge "
                                       "from the back benches', 'the leadership falls vacant'], 13) | has('member of "
                                       "parliament')) & (~had(['the campaign nobody gave a chance'], 13) | "
                                       "has('party leader'))",
                                'more': ["has('good name in town') | has('voice at the town hall') | has('a "
                                         "following in the party') | has('allies in the party')",
                                         "has('a loyal campaign team') | has('a list of supporters') | "
                                         "has('canvassing')",
                                         'time > .4'],
                                'less': ['stress > 1.5', 'money < .15', 'ago_move < sa']},
 'making peace with the long shot': {'anchor': "has('a long shot that missed') & had(['election night', 'a seat "
                                               "falls vacant', 'the leadership falls vacant', 'polling day for "
                                               "mayor', 'a challenge from the back benches', 'the campaign nobody "
                                               "gave a chance', 'writing in cold for a job in politics', 'the "
                                               "campaign loses its organiser'], 0.08333333333333333) & "
                                               '(ago_fail_long < 0.08333333333333333)',
                                     'req': 'age >= 25',
                                     'more': ['age >= 45', 'retired | (kids_home == 0)', 'ties > .5'],
                                     'less': ['stress > 1.5', 'health < .3']}})
# part politics LONGSHOTS LIFE
PACK_RULES.setdefault('politics', {}).setdefault('LIFE', {}).update({'standing with no party behind you': {'req': "~has('member of parliament') & ~has('parliamentary candidate') & "
                                              "((yrs_has('local councillor') >= 4) | (yrs_has('mayor') >= 2) | "
                                              "has('former member of parliament') | ((yrs_has('voice at the town "
                                              "hall') >= 6) & (has('activist in a cause') | has('union rep') | "
                                              "has('residents\\' committee member') | has('school-governance board "
                                              "member') | has('civil-liberties campaigner') | has('local hero'))))",
                                       'more': ["(yrs_has('local councillor') >= 8) | (yrs_has('mayor') >= 4)",
                                                "has('good name in town') | has('local hero') | has('a list of "
                                                "supporters') | has('a loyal campaign team')"],
                                       'less': ["has('party member')", 'stress > 1.5', 'money < .1']},
 'a run for mayor from outside the council': {'req': "~was('local councillor') & ~was('mayor') & ~has('mayoral "
                                                     "candidate') & ((yrs_has('local party officer') >= 4) | "
                                                     "(yrs_has('voice at the town hall') >= 5) | "
                                                     "(yrs_has('residents\\' committee member') >= 5) | "
                                                     "(yrs_has('school-governance board member') >= 4) | "
                                                     "(yrs_has('union rep') >= 5) | (yrs_has('local hero') >= 5) | "
                                                     "(yrs_has('good name in town') >= 10) | (yrs_has('founder of a "
                                                     "firm') >= 8) | (yrs_has('family business') >= 10) | "
                                                     "(yrs_has('party member') >= 6) | (yrs_has('activist in a "
                                                     "cause') >= 5))",
                                              'more': ["has('voice at the town hall') | has('local hero')",
                                                       'ago_move > 10'],
                                              'less': ['ago_move < 3', 'stress > 1.5']},
 'a challenge from the back benches': {'req': "(yrs_has('member of parliament') >= 4) & ~has('minister') & "
                                              "~has('party leader')",
                                       'more': ["yrs_has('member of parliament') >= 8",
                                                "has('a following in the party') | has('allies in the party')"],
                                       'less': ['stress > 1.5']},
 'the campaign nobody gave a chance': {'req': "(yrs_has('party leader') >= 2) & ~has('head of government')",
                                       'more': ["has('known across the country')"],
                                       'less': ['stress > 1.5']},
 'writing in cold for a job in politics': {'req': "~(has('political adviser') | has('party official') | "
                                                  "has('lobbyist') | has('policy analyst') | has('speechwriter') | "
                                                  "has('member of parliament')) & (age <= 70) & ((yrs_has('local "
                                                  "party officer') >= 1) | (has('graduate') & (yrs_has('data "
                                                  "analyst') >= 2)) | (yrs_has('salesperson') >= 3) | "
                                                  "(yrs_has('journalist') >= 3) | (yrs_has('constituency "
                                                  "caseworker') >= 1))",
                                           'more': ["has('graduate')",
                                                    "has('friend in power') | has('mentor')",
                                                    'time > .4'],
                                           'less': ['stress > 1.5']},
 'the campaign loses its organiser': {'req': "(age <= 75) & ~has('campaign organiser') & ~has('constituency "
                                             "caseworker') & ~has('pollster') & ~(has('political adviser') | "
                                             "has('party official') | has('lobbyist') | has('policy analyst') | "
                                             "has('speechwriter') | has('member of parliament'))",
                                      'more': ["(yrs_has('campaign volunteer') >= 3) | (yrs_has('local party "
                                               "officer') >= 3)",
                                               "has('canvassing')"],
                                      'less': ['stress > 1.5', 'time < .2']}})
# part science LONGSHOTS ECHO
PACK_RULES.setdefault('science', {}).setdefault('ECHO', {}).update({'the old door opens a crack': {'anchor': "has('a long shot that missed') & had(['a discovery nobody asked you for', "
                                          "'a group of your own, open to all comers', 'a facility looks outside for "
                                          "its next head', 'a search for a new voice for science', 'a chair falls "
                                          'vacant at another university\', "a scientist\'s post at a famous lab", '
                                          "'a named fellowship, one a year', 'a national centre opens its posts', "
                                          "'the survey wants a paid assistant'], 0.08333333333333333) & "
                                          '(ago_fail_long <= 0.08333333333333333)',
                                'req': "(age >= 28) & (age <= 85) & (health > .35) & ((had(['a discovery nobody "
                                       "asked you for'], 14) & ~has('independent investigator') & has('published "
                                       "research') & (has('research scientist') | has('research assistant') | "
                                       "has('citizen scientist') | has('community observer') | has('volunteer "
                                       "research organiser'))) | (had(['a group of your own, open to all comers'], "
                                       "14) & ~has('research group leader') & has('research grant') & (has('research "
                                       "scientist') | has('research project lead'))) | (had(['a facility looks "
                                       "outside for its next head'], 14) & ~has('research facility lead') & "
                                       "(has('lab work') | has('instrument troubleshooting')) & (has('laboratory "
                                       "technician') | has('research scientist'))) | (had(['a search for a new voice "
                                       "for science'], 14) & ~has('science communication specialist') & "
                                       "has('explaining science') & (has('research scientist') | has('research "
                                       "assistant') | has('journalist') | has('teacher'))) | (had(['a chair falls "
                                       "vacant at another university'], 14) & ~has('professor') & has('published "
                                       "research') & (has('research group leader') | has('research scientist'))) | "
                                       '(had(["a scientist\'s post at a famous lab"], 14) & ~has(\'research '
                                       "scientist') & (has('research assistant') | has('laboratory technician') | "
                                       "has('research data steward') | has('research software engineer'))) | "
                                       "(had(['a named fellowship, one a year'], 14) & ~has('postdoctoral "
                                       "researcher') & has('doctoral graduate') & has('research scientist') & "
                                       "(yrs_has('research scientist') <= 8)) | (had(['a national centre opens its "
                                       "posts'], 14) & has('research scientist')) | (had(['the survey wants a paid "
                                       "assistant'], 14) & ~has('research assistant') & (has('citizen scientist') | "
                                       "has('community observer'))))",
                                'more': ["has('mentor') | has('research collaborators')",
                                         "has('research grant') | has('savings') | has('patron')",
                                         "has('a finding that held up') | has('name in the field') | "
                                         "has('supervising researchers')"],
                                'less': ['stress > 1.5',
                                         'money < .15',
                                         'held_children & (kids_home > 0) & (time < .3)']},
 'the story of the long shot': {'anchor': "has('a long shot that missed') & had(['a discovery nobody asked you for', "
                                          "'a group of your own, open to all comers', 'a facility looks outside for "
                                          "its next head', 'a search for a new voice for science', 'a chair falls "
                                          'vacant at another university\', "a scientist\'s post at a famous lab", '
                                          "'a named fellowship, one a year', 'a national centre opens its posts', "
                                          "'the survey wants a paid assistant', 'the old door opens a crack'], "
                                          '0.08333333333333333) & (ago_fail_long <= 0.08333333333333333)',
                                'req': 'age >= 32',
                                'more': ['retired',
                                         'kids_home == 0',
                                         "has('teaching') | has('explaining science') | has('former students') | "
                                         "has('mentor')"],
                                'less': ['stress > 1.5', 'health < .25', 'ago_loss < 1']}})
# part science LONGSHOTS LIFE
PACK_RULES.setdefault('science', {}).setdefault('LIFE', {}).update({'a discovery nobody asked you for': {'req': "~has('independent investigator') & ((yrs_has('research scientist') >= "
                                             "2) | (yrs_has('research assistant') >= 3) | (has('published research') "
                                             "& ((yrs_has('citizen scientist') >= 5) | (yrs_has('community "
                                             "observer') >= 5) | (yrs_has('volunteer research organiser') >= 3))))"},
 'a group of your own, open to all comers': {'req': "~has('research group leader') & (yrs_has('research scientist') "
                                                    ">= 4) & has('research grant')"},
 'a facility looks outside for its next head': {'req': "~has('research facility lead') & ((yrs_has('laboratory "
                                                       "technician') >= 4) | (yrs_has('research scientist') >= 4)) & "
                                                       "(has('lab work') | has('instrument troubleshooting'))"},
 'a search for a new voice for science': {'req': "~has('science communication specialist') & (yrs_has('explaining "
                                                 "science') >= 3) & has('graduate') & (was('research scientist') | "
                                                 "was('research assistant') | was('journalist') | was('teacher'))"},
 'a chair falls vacant at another university': {'req': "~has('professor') & has('published research') & "
                                                       "((yrs_has('research group leader') >= 3) | "
                                                       "(yrs_has('research scientist') >= 8))"},
 "a scientist's post at a famous lab": {'req': "~has('research scientist') & has('graduate') & ((yrs_has('research "
                                               "assistant') >= 2) | (yrs_has('laboratory technician') >= 2) | "
                                               "(yrs_has('research data steward') >= 2) | (yrs_has('research "
                                               "software engineer') >= 2))"},
 'a named fellowship, one a year': {'req': "~has('postdoctoral researcher') & has('doctoral graduate') & "
                                           "(yrs_has('research scientist') <= 5) & (age <= 45)"},
 'a national centre opens its posts': {'req': "yrs_has('research scientist') >= 2"},
 'the survey wants a paid assistant': {'req': "~has('research assistant') & ((yrs_has('citizen scientist') >= 4) | "
                                              "(yrs_has('community observer') >= 4))"}})
# part stage BASE ECHO
PACK_RULES.setdefault('stage', {}).setdefault('ECHO', {}).update({'the part you never got to play': {'anchor': "had(['the school play'], 0.08333333333333333) & (age < 13)",
                                    'req': "(age >= 18) & ~has('amateur actor') & ~has('professional actor')",
                                    'more': ['(hR + hG) > .5', 'time > .5', "has('singing') | has('dancing')"],
                                    'less': ['stress > 1.5',
                                             'money < .15',
                                             'held_children & (kids_home > 0) & (time < .3)']},
 'never too late for the stage': {'anchor': "had(['the first months of retirement'], 0.08333333333333333)",
                                  'req': "retired & ~has('amateur actor') & (health > .4)",
                                  'more': ["was('amateur actor') | was('youth theatre member') | has('a lead role to "
                                           "remember')",
                                           'time > .5',
                                           '(hG + hR) > .45'],
                                  'less': ['health < .5', 'money < .15', 'held_partner & (support < .3)']},
 'the show you wrote to star in': {'anchor': "had(['inspiration strikes', 'wanting to be noticed'], "
                                             "0.08333333333333333) & has('acting')",
                                   'req': "(age >= 17) & ~has('lead actor or actress') & ~has('a fringe slot')",
                                   'more': ["has('writing stories') | has('writing scripts')",
                                            "has('improvisation')",
                                            '(hR + hU) > .5'],
                                   'less': ['stress > 1.5', 'money < .15', 'kids_home > 1']},
 'the part that came with the letter': {'anchor': "had(['an unexpected chance: a grant, a role, a stage'], "
                                                  "0.08333333333333333) & has('acting')",
                                        'req': "(age >= 17) & ~has('professional actor') & ((yrs_has('amateur "
                                               "actor') >= 2) | (yrs_has('background artist') >= 2) | "
                                               "(yrs_has('drama school student') >= 1))",
                                        'more': ["has('a lead role to remember')",
                                                 "has('amateur actor')",
                                                 "has('casting directory listing')"],
                                        'less': ['stress > 1.5', 'kids_home > 1', 'health < .4']}})
# part stage BASE LIFE
PACK_RULES.setdefault('stage', {}).setdefault('LIFE', {}).update({'the part of a lifetime is cast': {'req': "(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) | "
                                           "((yrs_has('amateur actor') >= 5) & has('a lead role to remember'))"},
 'chosen to wear the great mask': {'req': "(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) | "
                                          "((yrs_has('amateur actor') >= 5) & has('a lead role to remember'))"},
 'a glamour that makes the play real': {'req': "(yrs_has('professional actor') >= 2) | (yrs_has('voice actor') >= 2) "
                                               "| ((yrs_has('amateur actor') >= 5) & has('a lead role to "
                                               "remember'))"},
 'the understudy goes on': {'req': "has('understudy') & (yrs_has('professional actor') >= 1)"},
 'the director calls again': {'req': "has('a director who keeps casting you') & ((yrs_has('professional actor') >= "
                                     "2) | (yrs_has('voice actor') >= 2))"},
 'opening night at the fringe': {'req': "has('a fringe slot') & (has('professional actor') | has('voice actor') | "
                                        "(yrs_has('drama school student') >= 1) | (yrs_has('amateur actor') >= 2) | "
                                        "(yrs_has('background artist') >= 2))"},
 'a voice for the cartoon': {'req': "(yrs_has('professional actor') >= 1) | (has('accents and voices') & "
                                    "((yrs_has('amateur actor') >= 2) | (yrs_has('community-radio presenter') >= "
                                    '2)))'},
 'the stage management team is a person short': {'req': "(yrs_has('stage technician') >= 1) | (yrs_has('drama school "
                                                        "student') >= 1) | (yrs_has('amateur actor') >= 2) | "
                                                        "(yrs_has('community theatre director') >= 2)"},
 'a director is needed for the autumn play': {'req': "(~has('community theatre director') & ((yrs_has('amateur "
                                                     "actor') >= 3) | (yrs_has('drama teacher') >= 3))) | "
                                                     "(yrs_has('community theatre director') >= 3)"},
 'the script competition': {'req': "(yrs_has('novelist') >= 1) | (yrs_has('journalist') >= 1) | (((yrs_has('writing "
                                   "stories') >= 2) | (yrs_has('writing scripts') >= 2)) & (was('amateur actor') | "
                                   "was('community theatre director') | was('drama school student') | "
                                   "was('professional actor')))"},
 'the illusionist players come to town': {'req': "~has('amateur actor') | (yrs_has('amateur actor') >= 1)"},
 'the school needs someone to take drama': {'req': "has('acting') | was('amateur actor') | was('community theatre "
                                                   "director')"}})
# part stage BASE READ
PACK_RULES.setdefault('stage', {}).setdefault('READ', {}).update({'the reviews are in': {'req': "has('professional actor') | has('lead actor or actress') | has('director') | "
                               "has('playwright or screenwriter') | has('amateur actor') | has('community theatre "
                               "director')",
                        'more': ["has('lead actor or actress')", "has('a fringe slot')"],
                        'less': ["~has('lead actor or actress') & has('amateur actor')"]}})
# part stage LONGSHOTS ECHO
PACK_RULES.setdefault('stage', {}).setdefault('ECHO', {}).update({'the same door, years later': {'anchor': "has('a long shot that missed') & had(['the lead from the open queue', "
                                          "'filmed by chance in the street', 'the film you made with friends', 'the "
                                          "old theatre needs someone to save it', 'the late starter', 'the night "
                                          "both covers are off', 'the other side of the table', 'an open audition in "
                                          "the city', 'a voice for the cartoon', 'the stage management team is a "
                                          "person short', 'the old teller dies at midwinter', 'the illusionist "
                                          "players come to town'], 0.08333333333333333) & (ago_fail_long < "
                                          '0.08333333333333333)',
                                'req': "(age >= 21) & ~has('lead actor or actress') & ~has('artistic director')",
                                'more': ["has('acting') | has('writing scripts') | has('directing actors') | "
                                         "has('amateur actor')",
                                         '(hR + hB) > .5',
                                         'time > .4'],
                                'less': ['stress > 1.5', 'money < .15', 'health < .4']},
 'the long shot becomes a story to tell': {'anchor': "has('a long shot that missed') & had(['the lead from the open "
                                                     "queue', 'filmed by chance in the street', 'the film you made "
                                                     "with friends', 'the old theatre needs someone to save it', "
                                                     "'the late starter', 'the night both covers are off', 'the "
                                                     "other side of the table', 'an open audition in the city', 'a "
                                                     "voice for the cartoon', 'the stage management team is a person "
                                                     "short', 'the old teller dies at midwinter', 'the illusionist "
                                                     "players come to town'], 0.08333333333333333) & (ago_fail_long "
                                                     '< 0.08333333333333333)',
                                           'req': "(age >= 25) & ~has('lead actor or actress')",
                                           'more': ['sa > 10',
                                                    "has('teaching') | has('telling a story aloud') | has('acting')",
                                                    '(hW + hG) > .5'],
                                           'less': ['stress > 1.5', 'health < .3']}})
# part stage LONGSHOTS LIFE
PACK_RULES.setdefault('stage', {}).setdefault('LIFE', {}).update({'the lead from the open queue': {'req': "~has('lead actor or actress') & (has('professional actor') | has('voice "
                                         "actor') | has('understudy') | ((yrs_has('amateur actor') >= 5) & has('a "
                                         "lead role to remember')))"},
 'filmed by chance in the street': {'req': "~has('professional actor') & ~has('voice actor') & ((yrs_has('amateur "
                                           "actor') >= 3) | (yrs_has('background artist') >= 3))"},
 'the film you made with friends': {'req': "~has('playwright or screenwriter') & (has('novelist') | "
                                           "has('journalist') | was('amateur actor') | was('community theatre "
                                           "director') | was('professional actor') | was('drama school student'))"},
 'the old theatre needs someone to save it': {'req': "~has('artistic director') & ((yrs_has('director') >= 3) | "
                                                     "(yrs_has('community theatre director') >= 8))"},
 'the late starter': {'req': "~was('professional actor') & ~was('voice actor')"},
 'the night both covers are off': {'req': "~has('lead actor or actress')"},
 'the other side of the table': {'req': "~has('lead actor or actress')"}})
# ---- end of pasted pack conditions


# ---- outer world (W38, Library next3 §7): moments that make sense only with a technology. With the world on, such a
# moment does not come while the world lacks it (world_keys.TECH_KEYS); with the world off, nothing changes
PREMISE_TECH = {
    "new technology changes your job": "ai helper",
    "a friend wants to start a project with you": "internet",
    "learning to use a new phone": "phone",
    "the doctor says to stop driving": "car",
    "a match who wants to meet tonight": "online dating",
    "someone starts mocking you online": "internet",
    "a late raid with the online team": "internet",
    "the car keys after a few drinks": "car",
    "the cyclist at dusk": "car",
    "the spreadsheet the last clerk left behind": "computer",
    "the free app the volunteers want": "internet",
    "the town website's keeper wants out": "internet",
    "a dating app match": "online dating",
    "a heated argument online about politics": "internet",
}


# ---- outer world (W39, Library 10-07): existing moments that answer a cast member's want (world_keys.CAST_WANTS); the
# want's holder fills the moment's first who: slot. A moment's own cast_want: field wins
CAST_WANT = {
    "a friend asks to borrow money": "money", "a grown child asks for a loan": "money",
    "a friend says they are in love with you": "love",
    "a promotion is open": "rival", "a rival at work": "rival",
    "making peace with family you had cut off": "forgiveness",
    "your parents expect you home for the holidays": "home",
    "the owner wants to retire": "successor", "you are offered the top job": "successor",
    "a friend comes out to you": "secret",
}
