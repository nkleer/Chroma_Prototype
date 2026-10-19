# rules_world.py: part 11 of 11 of earth_rules.py, the engine's reading of the Library's words.
# The outer world's moments (PREMISE_TECH, CAST_WANT), pair moments, shadow seen, title stages.
# Lines here are earth_rules.py's own, unchanged: earth_rules.py joins the parts in order (RULES_PARTS) and runs
# them in its own namespace, so a name used here may be set in an earlier part. Never import or run it alone.
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

# stage 2 of the next update (the Library's notes/for-the-engine-stage2.md, 10-09): gates for the new inner moments.
# Pair moments (chroma-ideas/pair-moments.md): the pull, the meeting and the missing half, one each per pair of colours
PAIR_MOMENTS = {   # pair: (the pull, the meeting, the missing half)
    "WR": ("the timesheet a friend asks to fix", "a gang on the late bus", "the third missed session"),
    "WB": ("double pay to break the team's line", "the family purse", "the fortnight away"),
    "UR": ("a spare seat leaving in the morning", "a contraption in the shed", "answer by midnight"),
    "UG": ("the club's old paper booking book", "the plot in a dry summer", "the knee that never healed"),
    "BG": ("the captaincy a season early", "the skip outside the old shop", "the cottage and the offer"),
    "WU": ("the family meal done the old way", "the block's first set of rules", "the sums that never added up"),
    "UB": ("two evening classes and time for one", "a pattern nobody else has seen", "last year's answers"),
    "BR": ("money that arrives all at once", "a bonus and a birthday", "an unexpected sum"),
    "RG": ("the yearly trip with the whole group", "a summer under canvas", "the old crowd's night"),
    "GW": ("a front garden left to grow", "the empty lot on the street", "the wild corner"),
}
for (c1_, c2_), (pull_, meet_, miss_) in PAIR_MOMENTS.items():
    INNER[pull_] = dict(   # both in the identity, one of them rising over the last two years
        req=f"({c1_} > .22) & ({c2_} > .22) & ((rise('{c1_}') >= .04) | (rise('{c2_}') >= .04)) & ~had([{pull_!r}], 5)",
        more=[], less=[])
    INNER[meet_] = dict(   # the pair held together in the identity for two years or more
        req=f"({c1_} > .22) & ({c2_} > .22) & (pair_yrs('{c1_}', '{c2_}', .22) >= 2) & ~had([{meet_!r}], 5)",
        more=[], less=[])
    INNER[miss_] = dict(   # one high, its partner nearly gone (with item 2's "no counterweight")
        req=f"((({c1_} > .35) & ({c2_} < .10)) | (({c2_} > .35) & ({c1_} < .10))) & ~had([{miss_!r}], 4)",
        more=[], less=[])
# shadow reflections (chroma-ideas/shadows-mechanics.md §5, "seeing it"): two per shadow; the engine lowers the shadow
# part and marks it seen when one is met (engine.SH_REFL, from the moment's holds:)
SHADOW_SEEN = {"W": ("rigid", "the old words at the new desk", "the anniversary film at the club"),
               "U": ("indecisive", "we stopped asking you", "five notebooks, one list"),
               "B": ("ruthless", "learned from the best", "the birthday toast"),
               "R": ("reckless", "the video from the weekend", "your words in a young mouth"),
               "G": ("stuck in their ways", "the same cottage, nine years running", "in my day, played back")}
for c_, (st_, *nms_) in SHADOW_SEEN.items():
    for nm_ in nms_:   # the state held six months or more; at most once every three years for this shadow
        INNER[nm_] = dict(req=f"adj({st_!r}) & (yrs_adj({st_!r}) >= .5) & (sh_ago('{c_}') >= 3)", more=[], less=[])
# insight moments (chroma-ideas/curious-life.md C5): a long curiosity pays off; rare (about 1 life in 15, chance fitted)
INSIGHT = ["the night it all clicks", "the fault nobody else could find", "a pattern in years of notes",
           "a creature in none of the books", "an answer sixty years late"]
INSIGHT_CHANCE = 0.02   # weekly chance once the gate holds (to fit to about 1 life in 15 for the five together)
for nm_, yrs_, span_, extra_ in ((INSIGHT[0], 4, 4, ""), (INSIGHT[1], 8, 10, ""), (INSIGHT[2], 8, 10, ""),
                                 (INSIGHT[3], 8, 10, ""),
                                 (INSIGHT[4], 8, 10, " & (first_age(['a curiosity that will not let go']) < 15)")):
    INNER[nm_] = dict(req=f"((above_yrs('U', .25) >= {yrs_}) | (mk_span('learned a skill') >= {span_})){extra_}"
                          f" & ~had({INSIGHT!r}, 6) & chance({INSIGHT_CHANCE})", more=["hU > .3"], less=[])
# A16: the end of a national service term (earth-title-stages-own.lib): a soldier for a year or more, called up
INNER["the last parade of national service"] = dict(req="(yrs_has('soldier') >= 1) & had(['the call to serve'], 3)",
                                                    more=[], less=[])
