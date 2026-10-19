# Chroma content pack: Stage and Screen. The public callings' ladders, for aims version 1 (chroma-ideas/
# next-table-2026-10-19/plan.md, section 5). Pathways and packs thread, 2026-10-19.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims switch is on, so it changes no life. The format is set
# out in chroma-packs/tools/check_aims.py, which checks it (a short summary is at the top of ../politics/aims.py).
#
# One calling per road (PACK.md, "Road per color"), each road's lead colour with a second colour from its titles' and
# perks' ways, so the five faces make a ring (R B, B G, G W, W U, U R) and every colour stands in two of them.

AIMS_STAGE = {
    # R, acting and the lead: the star
    "to be a star": dict(
        face="R B", domain="career", sphere="arts",
        dreams=["a pop star"],
        tribal="to be the dancer every band waits to see", magic="to be the darling of the playhouses",
        steps=[
            dict(say="on a stage", any=["youth theatre member", "amateur actor", "drama school student",
                                        "background artist"]),
            dict(say="acting for a living", any=["professional actor", "understudy", "voice actor",
                                                 "casting directory listing"]),
            dict(say="a face people know", any=["a known face", "a lead role to remember", "good notices",
                                                "a cult following"], height="Known"),
            dict(say="the lead", any=["lead actor or actress", "an award for acting"], height="Notable"),
            dict(say="a household name", any=["a household name", "a work that outlives you"],
                 req="was('professional actor') | was('voice actor')", height="Historic"),
        ]),
    # U, writing, directing, voice and teaching: the one who writes what is played
    "to write what is played": dict(
        face="U R", domain="career", sphere="arts",
        dreams=[],
        tribal="to make the dances and tellings for the gatherings", magic="to write for the royal playhouse",
        steps=[
            dict(say="stories on paper", any=["writing scripts", "writing stories", "youth theatre member",
                                              "amateur actor"]),
            dict(say="a play of your own", any=["playwright or screenwriter", "a fringe slot"]),
            dict(say="people come to see your work", any=["good notices", "a cult following", "a company of your own"],
                 req="was('playwright or screenwriter') | has('writing scripts')", height="Known"),
            dict(say="a name across the country", any=["known across the country", "director"],
                 req="was('playwright or screenwriter')", height="Notable"),
            dict(say="a play still staged after you", any=["a work that outlives you"], height="Historic"),
        ]),
    # W, stage management, casting and running a theatre: the one who runs a theatre
    "to run a theatre": dict(
        face="W U", domain="career", sphere="arts",
        dreams=[],
        tribal="to order the dances of the great gathering", magic="to be master of the revels",
        steps=[
            dict(say="behind the scenes", any=["stage technician", "drama school student", "amateur actor",
                                               "youth theatre member"]),
            dict(say="running the show", any=["stage manager", "casting director", "calling the show"]),
            dict(say="the company trusts you", any=["good notices", "trusted with the keys",
                                                    "a director who keeps casting you"],
                 req="was('stage manager') | was('casting director') | was('director')", height="Known"),
            dict(say="a theatre to run", any=["director", "artistic director"], height="Notable"),
            dict(say="a theatre that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # B, producing and agents: the one who saves the old theatre
    "to save the old theatre": dict(
        face="B G", domain="career", sphere="arts",
        dreams=[],
        tribal="to keep the gathering's dances going, winter after winter", magic="to own the playhouse on the square",
        steps=[
            dict(say="a love of the stage", any=["amateur actor", "community theatre director", "background artist",
                                                 "stage technician"]),
            dict(say="putting shows on", any=["producer", "talent agent", "fundraising"]),
            dict(say="a company of your own", any=["a company of your own", "good name in town", "repeat fees"],
                 req="was('producer') | was('talent agent') | was('community theatre director')", height="Known"),
            dict(say="the theatre is yours", any=["artistic director", "known across the country"],
                 req="was('producer') | was('community theatre director')", height="Notable"),
            dict(say="a stage that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # G, community theatre and the extras: the one who gives the town its stage
    "to give the town its stage": dict(
        face="G W", domain="community", sphere="arts",
        dreams=[],
        tribal="to keep the band's dances and tellings", magic="to lead the town's mummers",
        steps=[
            dict(say="in the town's show", any=["youth theatre member", "amateur actor", "background artist",
                                                "telling a story aloud"]),
            dict(say="the town's players", any=["community theatre director", "drama teacher",
                                                "a company that feels like family"]),
            dict(say="the town comes to see", any=["a lead role to remember", "good name in town",
                                                   "name on the local scene"], height="Known"),
            dict(say="a stage for the whole country", any=["artistic director", "known across the country"],
                 req="was('community theatre director') | was('drama teacher')", height="Notable"),
            dict(say="a stage that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
}

# Who on the stage can earn [a work that outlives you] (core/legacy.py): years in the lead with the whole country
# knowing the face; a play still staged after years of good notices; a theatre led for a generation.
LEGACY_STAGE = ("(age >= 40) & (((yrs_has('lead actor or actress') >= 6) & has('known across the country')) | "
                "((yrs_has('playwright or screenwriter') >= 12) & (has('good notices') | has('a cult following'))) | "
                "(yrs_has('artistic director') >= 12) | ((yrs_has('director') >= 15) & has('good notices')))")
