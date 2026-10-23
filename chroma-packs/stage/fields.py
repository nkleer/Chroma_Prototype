# Chroma content pack: Stage and Screen. The five callings of aims.py as fields, for aims version 2 (v25, Emren's
# decision #9). Pathways and packs thread, 2026-10-23.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims_v2 is on and the pack is in batch.PACKS. Plain data;
# nothing is imported and nothing runs. The format is the Engine's frozen aims shape (chroma-engine/notes/v25/
# aims-shape.md in the shared folder, sections 3 and 8: the chess entry is the template); check_fields.py in
# ../tools checks it.
#
# Each field keeps its v1 aim (aims.py) as it is: the name, face, sphere, domain, tribal and magic, v1's dreams, and
# each step as a rung with its say, any, req and height unchanged. The dreams of core/dreams.py's AIM_DREAMS follow
# v1's. Shapes: the star and the one who writes what is played are the art shape (trying, showing, a following,
# recognised, a body of work), the one who runs a theatre the career shape (a foot in, established, senior, leading,
# the top), the one who saves the old theatre and the one who gives the town its stage the cause shape (caring,
# joining, organising, leading, a change that lasts); every shape has five rungs, so no field skips one.
#
# How the clocks were set. `years` is (median, 10th, 90th percentile) of steady effort from the rung below: the course
# lengths (drama school three years, the catalogue's lasts=3), the years a title needs in roles.py and in the moments'
# gates (engine-conditions.py: yrs_has, yrs_career), the legacy rule (aims.py LEGACY_STAGE: six years in the lead,
# twelve as a playwright or an artistic director, fifteen as a director), and estimates where nothing is counted, each
# named in the comment above its field. `share` is of those who keep at it, the share who reach the rung; the shares
# multiply down the ladder and were checked against the catalogue's share= of the rung's titles and its sources (the
# union rolls, the drama schools' places, the guilds, the amateur societies' surveys). `demand` is at steady
# intensity, outside paid work: hours a week, money a year and a one-time entry as shares of a year's free money, and
# how tiring it is. `window` names an external timing only where the step has one (the yearly script competitions and
# fringe); `upkeep` names the one part that really fades without use (an actor's agent and casting contacts, a stage
# manager's or a producer's companies and backers), never an achievement.

FIELDS_STAGE = {
    # Clock: UK drama schools take about 1,550 of 12,000 applicants a year for a 3-year course (catalogue); roles.py:
    # the other way in is 2 years with the local players or as an extra, with a union card, a listing or a fringe slot,
    # and the lead comes 2 years into a career; LEGACY_STAGE: 6 years in the lead, known across the country. Equity's
    # survey (most members earn little from acting) and the union rolls (professional actors about 4 lives in 1,000,
    # leads 1 in 1,000) for the shares. About 6 in 100 of those who keep at it reach Known, 18 in 1,000 the lead.
    "to be a star": dict(
        shape="art", face="R B", sphere="arts", domain="career", calling=True,
        dreams=["a pop star"],
        thing="the part", doing="acting", contest="an audition",
        places=["arts.stage", "arts.screen", "gather.hall"], prep=["performing"], meets=["meaning", "belonging"],
        people=dict(coach="a drama teacher who saw it in them first", rival="an actor up for the same parts",
                    peer="the rest of the company", patron="an agent who believes in them"),
        round=["the local players' next show", "a show of your own at the fringe",
               "the open auditions in the city, every spring"],
        below="{N} acts out every story at the dinner table, does all the voices and takes a bow at the end",
        tribal="to be the dancer every band waits to see", magic="to be the darling of the playhouses",
        rungs=[
            dict(say="on a stage", any=["youth theatre member", "amateur actor", "drama school student",
                                        "background artist"],
                 years=(1, 0.5, 2), share=0.9, start=(7, 18, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.03, entry=0.02, energy=0.4), window=None, upkeep=None),
            dict(say="acting for a living", any=["professional actor", "understudy", "voice actor",
                                                 "casting directory listing"],
                 years=(3.5, 1.5, 8), share=0.15, contests_y=6, forks=["pay", "take"],
                 demand=dict(hours=10, money=0.15, entry=0.3, energy=0.6), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "performing"])),
            dict(say="a face people know", any=["a known face", "a lead role to remember", "good notices",
                                                "a cult following"], height="Known",
                 years=(3, 1, 7), share=0.45, contests_y=6, forks=["take"],
                 demand=dict(hours=8, money=0.08, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="the lead", any=["lead actor or actress", "an award for acting"], height="Notable",
                 years=(4, 2, 10), share=0.3, contests_y=4, forks=["go_on", "take"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.7), window=None, upkeep=None),
            dict(say="a household name", any=["a household name", "a work that outlives you"],
                 req="was('professional actor') | was('voice actor')", height="Historic",
                 years=(8, 4, 20), share=0.08, contests_y=2, forks=["take"],
                 demand=dict(hours=5, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: roles.py: a playwright or screenwriter has 2 years of writing scripts and a stage rung behind them, or was
    # a novelist or a journalist; the script competitions and the fringe come once a year; LEGACY_STAGE: 12 years as
    # one with good notices. The writers' guilds' rolls (about 8 lives in 10,000, the catalogue) for the shares; the
    # rest estimate. About 8 in 100 of those who keep at it reach Known, 8 in 1,000 the country's notice.
    "to write what is played": dict(
        shape="art", face="U R", sphere="arts", domain="career", calling=True,
        dreams=["a playwright", "a maker of dances and tellings", "a writer for the royal playhouse"],
        thing="the play", doing="writing plays", contest="a script competition",
        places=["arts.stage", "arts.page", "arts.screen"], prep=["writing"], meets=["meaning", "autonomy"],
        people=dict(coach="a playwright who reads new scripts for the theatre",
                    rival="a writer whose play got the slot",
                    peer="the writers' group that reads its scenes aloud",
                    patron="a director who wants the next play first"),
        round=["a reading with actors in the room above a bar", "a short film made with friends",
               "the fringe festival, every year"],
        below="{N} writes plays for the cousins to put on at every family party, and directs them from the sofa",
        tribal="to make the dances and tellings for the gatherings", magic="to write for the royal playhouse",
        rungs=[
            dict(say="stories on paper", any=["writing scripts", "writing stories", "youth theatre member",
                                              "amateur actor"],
                 years=(1, 0.5, 3), share=0.9, start=(10, 25, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="a play of your own", any=["playwright or screenwriter", "a fringe slot"],
                 years=(4, 2, 9), share=0.3, contests_y=2, forks=["pay", "round"],
                 demand=dict(hours=10, money=0.1, entry=0.15, energy=0.5),
                 window=dict(every=1, open_weeks=10), upkeep=None),
            dict(say="people come to see your work", any=["good notices", "a cult following", "a company of your own"],
                 req="was('playwright or screenwriter') | has('writing scripts')", height="Known",
                 years=(4, 2, 8), share=0.3, contests_y=3, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0.05, energy=0.5), window=None, upkeep=None),
            dict(say="a name across the country", any=["known across the country", "director"],
                 req="was('playwright or screenwriter')", height="Notable",
                 years=(6, 3, 14), share=0.1, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a play still staged after you", any=["a work that outlives you"], height="Historic",
                 years=(6, 3, 15), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: roles.py: a stage manager has a year at the technician's bench or drama school, or 2 with the local
    # players; a director has 3 years as a stage manager, an actor or the players' director; LEGACY_STAGE: 12 years as
    # an artistic director or 15 as a director with good notices. Actors' Equity's stage-management weeks and TCG's
    # theatres (an artistic director about every ten years in each) for the shares, estimate. About 14 in 100 of those
    # who keep at it reach Known, 2 in 100 a theatre to run.
    "to run a theatre": dict(
        shape="career", face="W U", sphere="arts", domain="career", calling=True,
        dreams=["to run a theatre", "the one who orders the great dances", "master of the revels"],
        thing="the theatre", doing="running the show", contest="a first night",
        places=["arts.stage", "gather.hall", "learn.higher"], prep=["organising", "leading people"],
        meets=["competence", "belonging"],
        people=dict(coach="a stage manager who has called a thousand shows", rival="a deputy who wants the same job",
                    peer="the crew backstage", patron="the chair of a theatre's board who notices good work"),
        round=["a touring company that needs crew", "the local players, who always need hands backstage",
               "the summer festival's crew call, every year"],
        below="{N} runs the school play's props table with a list, a torch and a stopwatch, and no one misses a cue",
        tribal="to order the dances of the great gathering", magic="to be master of the revels",
        rungs=[
            dict(say="behind the scenes", any=["stage technician", "drama school student", "amateur actor",
                                               "youth theatre member"],
                 years=(1, 0.5, 3), share=0.9, start=(12, 22, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.02, entry=0.02, energy=0.4), window=None, upkeep=None),
            dict(say="running the show", any=["stage manager", "casting director", "calling the show"],
                 years=(3, 1.5, 6), share=0.35, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=8, money=0.05, entry=0.1, energy=0.6), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work"])),
            dict(say="the company trusts you", any=["good notices", "trusted with the keys",
                                                    "a director who keeps casting you"],
                 req="was('stage manager') | was('casting director') | was('director')", height="Known",
                 years=(4, 2, 8), share=0.45, contests_y=2, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a theatre to run", any=["director", "artistic director"], height="Notable",
                 years=(6, 3, 12), share=0.15, contests_y=3, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.7), window=None, upkeep=None),
            dict(say="a theatre that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(12, 8, 25), share=0.12, contests_y=2, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # Clock: roles.py: a producer has been a stage manager or a director, has a company of their own, or ran the local
    # players 3 years; an artistic director has 3 years as a director (the community director's long shot needs 8);
    # LEGACY_STAGE: 12 years as an artistic director. Producers are about 8 lives in 10,000, artistic directors 1 in
    # 10,000 (catalogue); the rest estimate. About 13 in 100 who keep at it reach Known, 13 in 1,000 the theatre.
    "to save the old theatre": dict(
        shape="cause", face="B G", sphere="arts", domain="career", calling=True,
        dreams=["to save the town's old theatre", "a theatre of one's own", "to keep the gathering's dances going",
                "the keeper of the dancing ground", "to own the playhouse on the square", "a patron of the players"],
        thing="the old theatre", doing="keeping the theatre going", contest="a funding bid",
        places=["arts.stage", "gather.hall", "rule.counsel"], prep=["organising", "the market"],
        meets=["belonging", "meaning"],
        people=dict(coach="a producer who saved a theatre once before",
                    rival="the developer who wants the building for flats", peer="the friends of the theatre",
                    patron="a local firm that backs the season"),
        round=["a season in the school hall while the roof is mended", "selling shares in the theatre to the town",
               "the friends' fundraising night, every month"],
        below="{N} sells raffle tickets door to door for new curtains in the school hall, and knows every buyer",
        tribal="to keep the gathering's dances going, winter after winter", magic="to own the playhouse on the square",
        rungs=[
            dict(say="a love of the stage", any=["amateur actor", "community theatre director", "background artist",
                                                 "stage technician"],
                 years=(1.5, 0.5, 4), share=0.9, start=(14, 35, 55), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="putting shows on", any=["producer", "talent agent", "fundraising"],
                 years=(4, 2, 9), share=0.4, contests_y=2, forks=["pay"],
                 demand=dict(hours=8, money=0.1, entry=0.1, energy=0.5), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "organising"])),
            dict(say="a company of your own", any=["a company of your own", "good name in town", "repeat fees"],
                 req="was('producer') | was('talent agent') | was('community theatre director')", height="Known",
                 years=(4, 2, 8), share=0.35, contests_y=2, forks=["pay", "take"],
                 demand=dict(hours=10, money=0.15, entry=0.2, energy=0.6), window=None, upkeep=None),
            dict(say="the theatre is yours", any=["artistic director", "known across the country"],
                 req="was('producer') | was('community theatre director')", height="Notable",
                 years=(8, 4, 15), share=0.1, contests_y=2, forks=["take"],
                 demand=dict(hours=12, money=0.15, entry=0.3, energy=0.7), window=None, upkeep=None),
            dict(say="a stage that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(12, 8, 25), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # Clock: roles.py: a community theatre director has 4 years as an amateur actor; NODA's survey (437,800 taking part
    # in about 2,400 societies) and AACT (about 7,000 community theatres) for the wide shares of the first rungs;
    # artistic directors are 1 life in 10,000 (TCG, the catalogue); LEGACY_STAGE: 12 years as one. About 22 in 100 of
    # those who keep at it reach Known, 7 in 1,000 the country's stage.
    "to give the town its stage": dict(
        shape="cause", face="G W", sphere="arts", domain="community", calling=True,
        dreams=["to give the town a stage of its own", "a keeper of the band's tellings", "to lead the town's mummers"],
        thing="the town's show", doing="putting on the town's show", contest="a drama festival",
        places=["gather.hall", "arts.stage"], prep=["performing", "organising"], meets=["belonging", "meaning"],
        people=dict(coach="the old director of the local players",
                    rival="the other society in town that always gets the hall first",
                    peer="the cast and crew of neighbours", patron="the head teacher who lends the school hall"),
        round=["a show in the village hall when the theatre is booked", "a play read aloud at the library",
               "the local players' casting night, every autumn"],
        below="{N} gathers the street's children every summer to put on a show in the garden, with sheets for curtains",
        tribal="to keep the band's dances and tellings", magic="to lead the town's mummers",
        rungs=[
            dict(say="in the town's show", any=["youth theatre member", "amateur actor", "background artist",
                                                "telling a story aloud"],
                 years=(1, 0.5, 3), share=0.9, start=(8, 35, 65), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="the town's players", any=["community theatre director", "drama teacher",
                                                "a company that feels like family"],
                 years=(4, 2, 10), share=0.45, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0.02, energy=0.5), window=None, upkeep=None),
            dict(say="the town comes to see", any=["a lead role to remember", "good name in town",
                                                   "name on the local scene"], height="Known",
                 years=(3, 1, 7), share=0.55, contests_y=2, forks=["round"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a stage for the whole country", any=["artistic director", "known across the country"],
                 req="was('community theatre director') | was('drama teacher')", height="Notable",
                 years=(10, 5, 20), share=0.03, contests_y=2, forks=["take"],
                 demand=dict(hours=10, money=0.05, entry=0.05, energy=0.6), window=None, upkeep=None),
            dict(say="a stage that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(12, 8, 25), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),
}
