# Suggested engine conditions for the SECOND set of child inner moments and child outside events (for earth_rules.INNER / READ),
# drafts/earth-child-inner-2.lib and drafts/earth-child-events-2.lib. Same format as staging/child-rules-proposal.py.
#
# Thresholds are at children's measured levels (scratch run of the full batch, 300 lives, ages 5 to 12, 10th / 50th / 90th):
#   safety .64 / .79 / .84   belonging .46 / .64 / .76   autonomy .53-.63 / .76-.81 / .87-.90   competence .44-.51 / .58-.63 / .68-.71
#   meaning .59-.63 / .72-.76 / .78-.82   money .13-.16 / .15-.18 / .16-.20   time .65 / .65-.70 / .70
#   stress .35 / .58 / .84-.90   peace .28-.34 / .40-.46 / .49-.55   support .24 / .34 / .44   react .96-1.0 / 1.03-1.08 / 1.11-1.19
#   steady .03-.08 / .06-.14 / .11-.23   outlook .18-.22 / .23-.27 / .28-.32   hW..hG .17 / .20 / .21-.25 (ten-year shares start even)
#   fails13 3.3-3.8 / 4.9-5.4 / 6.5-7.1 (so "fails13 >= 2" is always true in childhood); n_dream, n_passion 0; ago_hard always 99.
# So "steady > .6", "react > 1.2", "hX > .3", "hX + hY > .45", "support > .6", "time < .15" never hold for a child, and
# "money < .2", "outlook < .4", "time > .5" always hold. This set uses steady > .15, react > 1.1, hX > .22, sums > .42,
# support > .4, money < .12 / .14, stress > 1.2 for "rare" stress. INNER_CHILD_FIX / READ_CHILD_FIX below offer the same for the first set.
INNER_CHILD = {
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
READ_CHILD = {
    # ---- joys
    "your birthday party": dict(less=["money < .12", "ago_move < .25"]),
    "a week with the grandparents": dict(req="alive_grandparent > 0", more=["alive_grandparent >= 3"]),
    "fireworks night": dict(less=["harsh > 0", "unrest > 0"]),
    "the Saturday team wins at last": dict(more=["competence > .65"]),
    "a parcel just for you": dict(more=["alive_grandparent >= 3"]),
    "a day out at the zoo": dict(less=["money < .12", "harsh > 0"]),
    "something lost turns up": dict(),
    # ---- troubles
    "an arm in a cast for six weeks": dict(more=["hR > .22"]),
    "a bad school report": dict(more=["competence < .55", "ago_move < 1", "stress > .9"], less=["competence > .7"]),
    "a grandparent goes into hospital": dict(req="alive_grandparent > 0", more=["alive_grandparent >= 3"]),
    "the big kids take over the playground": dict(more=["belonging < .5"]),
    "told off in front of the class": dict(more=["hR > .22", "react > 1.1"], less=["hW > .22"]),
    "the cat goes missing": dict(),
    "no holiday this year": dict(more=["money < .13", "harsh > 0"], less=["money > .2"]),
}

# Optional, for the FIRST set (already in earth_rules.INNER_CHILD / READ_CHILD): the same likelier / rarer lines with
# thresholds a child can reach. Only "more" and "less" change; every "req" stays as the engine took it, so the rates the
# first set was calibrated at hold (its req clauses "fails13 >= 1 / 2" are always true and "support > .6" never, as noted).
# Apply with: for k, v in INNER_CHILD_FIX.items(): INNER[k].update(v)   (and the same for READ).
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
