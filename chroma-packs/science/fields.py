# Chroma content pack: Science. The pack's five aims as fields, for aims version 2 (Emren's v25 decision #9, "Every
# held aim, shared capacity and worthwhile development"). Pathways and packs thread, 2026-10-23, to the writers' brief
# (chroma-ideas/v25-prep/packs/fields/BRIEF.md).
#
# SWITCHED OFF: nothing reads this file until the Engine's aims_v2 is on and the pack is in batch.PACKS, so it changes
# no life. The format is the Engine's frozen aims shape (chroma-engine/notes/v25/aims-shape.md, sections 3 and 8: the
# chess entry, key for key, with the keys section 3 adds: demand, window, upkeep, prep and meets);
# chroma-packs/tools/check_fields.py checks it. FIELDS_SCIENCE = {aim: field}, one field for each aim of aims.py (v1),
# under the same name. Each keeps v1's face, sphere, domain, tribal and magic, and v1's steps in order as its rungs
# (say, any, req and height unchanged); its dreams are v1's, then the aim's dreams from core/dreams.py (AIM_DREAMS).
# Shapes: the lab is a career ("to build a great lab"); the living world, the evidence, the long record and the
# explaining are knowledge. Every shape here has 5 rungs, as every aim has 5 steps, so no skip.
#
# How the clocks were set. `years` is (median, 10th, 90th percentile) of steady effort from the rung below, read from
# the catalogue's sources (OECD: about 10 researchers per 1,000 in work, about 1.1 to 1.3 adults in 100 with a
# doctorate), the usual training (a first degree of 3 to 4 years, a doctorate of 3 to 6 more, postdoctoral posts of 2
# to 6), the years roles.py and the long shots' gates ask of a title (yrs_has, yrs_career), and LEGACY_SCIENCE in
# aims.py (the Historic rung asks age 40 and 8 to 15 years at the top with a finding, a method or a dataset others
# keep using); the rest is estimate, and the comment above each field says which. `share` is, of those who keep at
# it, the share who reach the rung; the shares multiply down the ladder, and the products were held against the
# catalogue's share= (a research scientist about 1 life in 80, a group leader or a professor 1 in 500, the head of a
# facility 1 in 2,000) and its estimates (about one scientist in two leads a project, one in six a group): about 1 in
# 6 of those who keep at it reach the Known rung, 2 to 4 in 100 the top of the field, and under half a percent the
# Historic rung. `start` is when the interest usually comes (a child's collection or notebook from 8 to 12, the
# subject chosen at school or college by the early twenties); the odds fall after late_from but never shut.
#
# `demand` is at steady intensity: hours a week of free time (a research post is the job itself, so it counts only
# the extra evenings and weekends; the volunteer counts and the study are free time), money a year and a one-time
# entry cost as shares of a year's free money (a degree's fees .25 a year and .3 to enter, a binocular and a notebook
# .02), and how tiring it is. `window` marks the real external timing only: the yearly funding round (a call open about
# 10 weeks) that a first grant and a group of one's own need, and the head of a station, an appointment made when the
# post falls vacant (one in reach about every 4 years: estimate). `upkeep` only where a benefit really fades: the
# hands at the bench and the field without practice (proficiency, about 5 years), collaborators and an audience
# without new work (access); a finding published, a dataset kept or a name made stays.

FIELDS_SCIENCE = {
    # Clock: OECD (doctorates, in the catalogue); a first degree of 3 to 4 years and a doctorate of 3 to 6; roles.py (a
    # research assistant with a degree, a scientist from a doctorate or from an assistant's years); the catalogue (about
    # one scientist in six leads a group; professors about 25,000 at a time in the UK); LEGACY_SCIENCE asks 8 years as a
    # professor or 10 at the head of a group. The years from a group to the Historic rung: estimate.
    "to understand the living world": dict(
        shape="knowledge", face="U G", sphere="learn", domain="career", calling=True,
        dreams=["a scientist", "a gatherer who knows every plant", "a vet"],
        thing="the living world", doing="studying living things", contest="a paper sent to the reviewers",
        places=["prod.wild", "learn.higher", "learn.keeping"], prep=["research", "study", "the land"],
        meets=["competence", "meaning"],
        people=dict(coach="a field biologist who takes students out every summer",
                    rival="a student in the same lab chasing the same question", peer="the others at the field station",
                    patron="a professor who finds them a place"),
        round=["a survey that takes volunteers", "a lab in another town with a place free",
               "the count at the nature reserve, every month"],
        below="{N} lies on the lawn for an hour watching the ants carry a crumb, and draws a map of where they go",
        tribal="to know the land and its creatures better than anyone living",
        magic="to be a naturalist of the academy",
        rungs=[
            dict(say="watching closely", any=["citizen scientist", "community observer", "fieldwork",
                                              "a nose for the odd result"],
                 years=(1, 0.5, 3), share=0.9, start=(8, 18, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="research of your own", any=["research assistant", "participatory research coordinator",
                                                  "field permit", "a research project under way"],
                 years=(4, 2, 7), share=0.5, contests_y=1, forks=["pay"],
                 demand=dict(hours=12, money=0.25, entry=0.3, energy=0.55), window=None, upkeep=None),
            dict(say="a name in the field", any=["research scientist", "published research", "name in the field"],
                 height="Known",
                 years=(5, 3, 9), share=0.4, contests_y=2, forks=["take"],
                 demand=dict(hours=10, money=0.08, entry=0.1, energy=0.6), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["research", "teaching"])),
            dict(say="at the top of the field", any=["professor", "research group leader", "independent investigator"],
                 height="Notable",
                 years=(8, 4, 15), share=0.2, contests_y=2, forks=["take", "round"],
                 demand=dict(hours=10, money=0.03, entry=0.05, energy=0.7),
                 window=dict(every=1, open_weeks=10), upkeep=None),
            dict(say="a discovery that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(10, 6, 25), share=0.12, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),
    # Clock: a first degree, then a research assistant's post or a doctorate (3 to 6 years); a first grant of one's own
    # usually after a doctorate and a postdoctoral post or two; roles.py (a project lead after 3 years in research with
    # a grant, a group leader after 6 with a grant and published work); the catalogue (one scientist in two leads a
    # project, one in six a group); LEGACY_SCIENCE asks 10 years at the head of a group or 8 as a professor. Shares:
    # estimate.
    "to build a great lab": dict(
        shape="career", face="B R", sphere="learn", domain="career", calling=True,
        dreams=["to lead a great laboratory", "a leader of the finders", "to found a school at the academy"],
        thing="the lab", doing="building the lab", contest="a grant panel",
        places=["learn.higher", "learn.keeping"], prep=["research", "leading people", "organising"],
        meets=["competence", "autonomy"],
        people=dict(coach="a senior scientist who has built two labs already",
                    rival="a group across the corridor chasing the same grant", peer="the other new group leaders",
                    patron="a funder who backs bold ideas"),
        round=["a smaller funder that takes risks", "a partnership with a company's lab",
               "the funding round, every year"],
        below="{N} turns the garden shed into a laboratory and signs up the younger cousins as assistants",
        tribal="to lead the band's finders of new ways", magic="to found a school of one's own at the academy",
        rungs=[
            dict(say="a first project", any=["research assistant", "grant writing", "doctoral graduate"],
                 years=(3.5, 2, 6), share=0.85, start=(15, 22, 35), contests_y=0, forks=["pay"],
                 demand=dict(hours=12, money=0.25, entry=0.3, energy=0.5), window=None, upkeep=None),
            dict(say="a project of your own", any=["research project lead", "a research project under way",
                                                   "research grant", "a loyal research team"],
                 years=(5, 3, 9), share=0.4, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=10, money=0.05, entry=0.05, energy=0.65),
                 window=dict(every=1, open_weeks=10), upkeep=None),
            dict(say="a method others use", any=["a method others use", "research collaborators", "name in the field"],
                 height="Known",
                 years=(4, 2, 8), share=0.45, contests_y=1, forks=["go_on"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.6), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["research", "collaboration"])),
            dict(say="a group that leads the field", any=["research group leader", "professor",
                                                          "research facility lead"], height="Notable",
                 years=(6, 3, 12), share=0.2, contests_y=2, forks=["take"],
                 demand=dict(hours=12, money=0.04, entry=0.05, energy=0.75),
                 window=dict(every=1, open_weeks=10), upkeep=None),
            dict(say="a school that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(12, 6, 25), share=0.12, contests_y=1, forks=["go_on"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
    # Clock: a first degree or a journalist's training, then a first post in a museum, a press office or a newsroom
    # (roles.py: a communicator with a degree and the knack of explaining, or from a research post or journalism); the
    # long shot's gate asks 3 years of explaining science; the reach ladder (core/reach.py: a household name after 3
    # years known across the country); LEGACY_SCIENCE asks 15 years as a communicator. Shares: estimate.
    "to make the world understand": dict(
        shape="knowledge", face="R W", sphere="learn", domain="career", calling=True,
        dreams=["to explain science to everyone", "a teller of the sky", "a lecturer to the commons"],
        thing="science", doing="explaining science", contest="a public lecture",
        places=["arts.screen", "arts.page", "learn.keeping"], prep=["writing", "public speaking", "study"],
        meets=["meaning", "belonging"],
        people=dict(coach="a broadcaster who began as a scientist", rival="a presenter who gets the slots they wanted",
                    peer="the other writers on the science desk", patron="a producer who gives them a first slot"),
        round=["a column in the local paper", "talks in schools that ask for a speaker",
               "the science evening at the library, every month"],
        below="{N} explains to the whole table why the moon changes shape, and draws it on a napkin to make sure",
        tribal="to be the one who explains the sky and the seasons to the bands",
        magic="to be the academy's voice in the square",
        rungs=[
            dict(say="explaining it well", any=["explaining science", "citizen scientist", "community-radio presenter"],
                 years=(1, 0.5, 3), share=0.9, start=(12, 25, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.01, entry=0.01, energy=0.3), window=None, upkeep=None),
            dict(say="telling it for a living", any=["science communication specialist", "journalist", "press card"],
                 years=(4, 2, 8), share=0.35, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.15, entry=0.25, energy=0.5), window=None, upkeep=None),
            dict(say="people listen", any=["following online", "name in the field", "good name in town"],
                 req="was('science communication specialist') | was('journalist') | has('explaining science')",
                 height="Known",
                 years=(4, 2, 9), share=0.5, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0.02, energy=0.45), window=None,
                 upkeep=dict(of="access", years=2, kept_by=["work", "writing", "performing"])),
            dict(say="known across the country", any=["known across the country"],
                 req="was('science communication specialist') | was('journalist')", height="Notable",
                 years=(7, 3, 15), share=0.12, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="a household name", any=["a household name", "a work that outlives you"],
                 req="was('science communication specialist') | was('journalist')", height="Historic",
                 years=(8, 3, 20), share=0.12, contests_y=1, forks=["take", "go_on"],
                 demand=dict(hours=8, money=0.03, entry=0.02, energy=0.6), window=None, upkeep=None),
        ]),
    # Clock: the careful habits come with a first research post after a degree (roles.py: research integrity, evidence
    # synthesis and reproducible workflows are learned on research jobs); an evidence synthesis specialist from years
    # as an assistant or scientist; a finding others repeat usually some years after the first papers; the authority
    # rungs as in "to understand the living world"; LEGACY_SCIENCE as there. Shares: estimate.
    "to get it right": dict(
        shape="knowledge", face="W U", sphere="learn", domain="career", calling=True,
        dreams=["a scientist whose work stands", "a keeper of true knowledge", "a master of the archives"],
        thing="the evidence", doing="checking the evidence", contest="a result put to the test",
        places=["learn.keeping", "learn.higher"], prep=["research", "numbers", "reading"],
        meets=["competence", "meaning"],
        people=dict(coach="a statistician who checks every claim twice",
                    rival="a scientist whose bold claims get the headlines", peer="the reviewers who meet each month",
                    patron="an editor who trusts their reviews"),
        round=["a review group that takes volunteers", "another lab's open data, checked from home",
               "the journal club, every week"],
        below="{N} weighs the bag of sweets on the kitchen scale to check that the packet is telling the truth",
        tribal="to be the one who keeps the band's knowledge true", magic="to be a master of the archives",
        rungs=[
            dict(say="careful work", any=["research integrity", "evidence synthesis", "reproducible workflow"],
                 years=(3, 1.5, 6), share=0.85, start=(14, 22, 40), contests_y=0, forks=["pay"],
                 demand=dict(hours=10, money=0.2, entry=0.3, energy=0.45), window=None, upkeep=None),
            dict(say="checking the evidence", any=["evidence synthesis specialist", "research assistant",
                                                   "ethics approval"],
                 years=(3, 1, 6), share=0.6, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a finding that held up", any=["a finding that held up", "published research"], height="Known",
                 years=(5, 2, 10), share=0.35, contests_y=2, forks=["go_on"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="the field's authority", any=["research group leader", "professor"], height="Notable",
                 years=(9, 4, 16), share=0.15, contests_y=2, forks=["take", "round"],
                 demand=dict(hours=10, money=0.03, entry=0.05, energy=0.7),
                 window=dict(every=1, open_weeks=10), upkeep=None),
            dict(say="a finding that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(10, 5, 25), share=0.15, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),
    # Clock: long-term monitoring volunteers keep a station or a count for years (the catalogue's community observer);
    # roles.py (a data steward from an assistant's or a data analyst's years with data skills; a dataset others use
    # after 5 years in research with a reproducible workflow); a monitoring record usually needs a decade or more before
    # others build on it; the head of a station from 4 years in post (roles.py); LEGACY_SCIENCE asks 10 years at its
    # head. Shares: estimate (shared facilities are few, each with one head).
    "to keep the long record": dict(
        shape="knowledge", face="G B", sphere="learn", domain="career", calling=True,
        dreams=["to keep a record of the world that lasts", "a counter of the seasons",
                "a keeper of the observatory's tables"],
        thing="the record", doing="keeping the record", contest="a check of the record",
        places=["prod.wild", "learn.keeping"], prep=["research", "numbers", "the land"],
        meets=["meaning", "competence"],
        people=dict(coach="an old observer who has kept the same record for forty years",
                    rival="a station that wants the same money", peer="the volunteers on the rota",
                    patron="a scientist who builds on the numbers"),
        round=["a station in the next valley that needs a keeper", "the archive's old ledgers, typed up at home",
               "the readings at the same spot, every morning"],
        below="{N} writes down the temperature at the back door in a notebook every morning, and has not missed a day "
              "since the spring",
        tribal="to be the keeper of the band's counts of the seasons", magic="to keep the observatory's long tables",
        rungs=[
            dict(say="keeping count", any=["community observer", "volunteer research organiser",
                                           "reproducible workflow"],
                 years=(1, 0.5, 3), share=0.9, start=(10, 25, 55), contests_y=0, forks=["go_on"],
                 demand=dict(hours=2, money=0.01, entry=0.02, energy=0.25), window=None, upkeep=None),
            dict(say="a record in your care", any=["research data steward", "participatory research coordinator",
                                                   "community partners"],
                 years=(5, 2, 10), share=0.35, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.1, entry=0.2, energy=0.4), window=None, upkeep=None),
            dict(say="a record others use", any=["a dataset others use", "name in the field"], height="Known",
                 years=(8, 4, 15), share=0.45, contests_y=1, forks=["go_on"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.35), window=None, upkeep=None),
            dict(say="head of the station", any=["research facility lead"], height="Notable",
                 years=(7, 3, 15), share=0.12, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0.05, energy=0.6),
                 window=dict(every=4, open_weeks=8), upkeep=None),
            dict(say="a record that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(10, 5, 25), share=0.15, contests_y=1, forks=["go_on"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),
}
