# Chroma content pack: Science. The public callings' ladders, for aims version 1 (chroma-ideas/next-table-2026-10-19/
# plan.md, section 5). Pathways and packs thread, 2026-10-19.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims switch is on, so it changes no life. The format is set
# out in chroma-packs/tools/check_aims.py, which checks it (a short summary is at the top of ../politics/aims.py).
#
# One calling per road (PACK.md, "Roads per color"), each road's lead colour with a second colour from its titles' and
# perks' ways, so the five faces make a ring (W U, U G, G B, B R, R W) and every colour stands in two of them.

AIMS_SCIENCE = {
    # U, the lab researcher: the naturalist (fieldwork and the odd result, read through the colours of the living world)
    "to understand the living world": dict(
        face="U G", domain="career", sphere="learn",
        dreams=["a scientist", "a gatherer who knows every plant", "a vet"],
        tribal="to know the land and its creatures better than anyone living", magic="to be a naturalist of the academy",
        steps=[
            dict(say="watching closely", any=["citizen scientist", "community observer", "fieldwork",
                                              "a nose for the odd result"]),
            dict(say="research of your own", any=["research assistant", "participatory research coordinator",
                                                  "field permit", "a research project under way"]),
            dict(say="a name in the field", any=["research scientist", "published research", "name in the field"],
                 height="Known"),
            dict(say="at the top of the field", any=["professor", "research group leader", "independent investigator"],
                 height="Notable"),
            dict(say="a discovery that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # B, the research leader: the one who builds a great lab
    "to build a great lab": dict(
        face="B R", domain="career", sphere="learn",
        dreams=[],
        tribal="to lead the band's finders of new ways", magic="to found a school of one's own at the academy",
        steps=[
            dict(say="a first project", any=["research assistant", "grant writing", "doctoral graduate"]),
            dict(say="a project of your own", any=["research project lead", "a research project under way",
                                                   "research grant", "a loyal research team"]),
            dict(say="a method others use", any=["a method others use", "research collaborators", "name in the field"],
                 height="Known"),
            dict(say="a group that leads the field", any=["research group leader", "professor",
                                                          "research facility lead"], height="Notable"),
            dict(say="a school that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # R, the communicator: the one who makes the world understand
    "to make the world understand": dict(
        face="R W", domain="career", sphere="learn",
        dreams=[],
        tribal="to be the one who explains the sky and the seasons to the bands",
        magic="to be the academy's voice in the square",
        steps=[
            dict(say="explaining it well", any=["explaining science", "citizen scientist", "community-radio presenter"]),
            dict(say="telling it for a living", any=["science communication specialist", "journalist", "press card"]),
            dict(say="people listen", any=["following online", "name in the field", "good name in town"],
                 req="was('science communication specialist') | was('journalist') | has('explaining science')",
                 height="Known"),
            dict(say="known across the country", any=["known across the country"],
                 req="was('science communication specialist') | was('journalist')", height="Notable"),
            dict(say="a household name", any=["a household name", "a work that outlives you"],
                 req="was('science communication specialist') | was('journalist')", height="Historic"),
        ]),
    # W, the evidence and the shared record: the one who gets it right
    "to get it right": dict(
        face="W U", domain="career", sphere="learn",
        dreams=[],
        tribal="to be the one who keeps the band's knowledge true", magic="to be a master of the archives",
        steps=[
            dict(say="careful work", any=["research integrity", "evidence synthesis", "reproducible workflow"]),
            dict(say="checking the evidence", any=["evidence synthesis specialist", "research assistant",
                                                   "ethics approval"]),
            dict(say="a finding that held up", any=["a finding that held up", "published research"], height="Known"),
            dict(say="the field's authority", any=["research group leader", "professor"], height="Notable"),
            dict(say="a finding that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # G, the place, the facility and the long record: the one who keeps the long record
    "to keep the long record": dict(
        face="G B", domain="career", sphere="learn",
        dreams=[],
        tribal="to be the keeper of the band's counts of the seasons", magic="to keep the observatory's long tables",
        steps=[
            dict(say="keeping count", any=["community observer", "volunteer research organiser",
                                           "reproducible workflow"]),
            dict(say="a record in your care", any=["research data steward", "participatory research coordinator",
                                                   "community partners"]),
            dict(say="a record others use", any=["a dataset others use", "name in the field"], height="Known"),
            dict(say="head of the station", any=["research facility lead"], height="Notable"),
            dict(say="a record that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
}

# Who in science can earn [a work that outlives you] (core/legacy.py): years at the top of the field with a finding, a
# method or a dataset others keep using; or a lifetime explaining science to the whole country.
LEGACY_SCIENCE = ("(age >= 40) & ((((yrs_has('professor') >= 8) | (yrs_has('research group leader') >= 10) | "
                  "(yrs_has('research facility lead') >= 10) | (yrs_has('independent investigator') >= 10)) & "
                  "(has('a finding that held up') | has('a method others use') | has('a dataset others use'))) | "
                  "((yrs_has('science communication specialist') >= 15) & has('known across the country')))")
