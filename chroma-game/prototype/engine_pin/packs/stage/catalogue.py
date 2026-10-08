# Chroma content pack: Stage and Screen: Acting, Theatre, Film and Television (modern Earth). Catalogue: titles and
# perks. Pathways and packs thread, 2026-10-06. Draft for Emren's review, not live. Emren's ask for the pack (packs
# thread, 01:31): "You can also work on third content package, you can choose the concept name subject and its content
# as you seem fit. Lead actor/actresss availability must be inside with all new content." So the lead is reachable on
# every road the pack opens: amateur, youth and school, fringe and one-person shows, stage, screen, voice, late life, and
# the tribal and magic worlds (PACK.md, "The lead on every road"). Plain data in the fields of
# chroma-library/earth_perks_titles.py (its header defines every field); nothing is imported and nothing runs. Modern
# Earth terms, as the base catalogue (no worlds field); the forms of every title and perk in the tribal and magic worlds
# are in worlds.py next to this file.
#
# The pack only adds. It reuses the base catalogue's [stage technician], [sound engineer], [novelist], [teacher],
# [festival organiser], [community-radio presenter], [stagecraft], [singing], [dancing], [writing stories], [public
# speaking], [following online], [name on the local scene], [good name in town], [mentor], [patron], [contact in the
# trade], [cleared to work with children], [teaching], [graduate], [scholarship], [savings], [striking a deal],
# [organising people], [selling], [second language], [boxing or martial arts] and [reliable record] instead of
# repeating them. The reach ladder ([known across the country], [a household name]) is shared by every pathway pack:
# chroma-packs/core/reach.py. Music, dance and comedy belong to a later Music and Performance pack, novels and visual
# art to a later Art and Writing pack (PACK.md, "Boundaries with other packs").
#
# Choices, on purpose (PACK.md, "Departures"):
#   - [lead actor or actress] is a facet (the engine's refines) held on top of [professional actor] or [voice actor],
#     with its own ways and profiles: a lead is a part, not a job, so it lasts a run or a series and the actor goes on
#     acting after it. The amateur, the child and the one-person show lead through the standing perk [a lead role to
#     remember] instead, which every road can reach.
#   - [artistic director] is a facet on [director], as a director keeps directing while running a theatre.
#   - [background artist] is a community title, held next to a day job, as nearly every extra works another job.
#   - [drama school student] and [understudy] are statuses: a three-year course, and a part learned for one run.
#   - No child holds a career title: a child performs through [youth theatre member], [a lead role to remember] and
#     [child performance licence] (a chaperone, a licence, school hours), never a contract of their own.
#   - Perks carry ways (colors), balanced over the five colors, as in the Science and Politics packs.
#
# Shares: share of people in a modern rich country who ever hold it. Sources: US Bureau of Labor Statistics (May 2023:
# 62,560 employed actors, median 20.50 dollars an hour; 154,470 producers and directors; 12,870 agents and business
# managers of artists, performers and athletes), Equity UK (48,606 members in 2024; its survey: 48 in 100 earned under
# 6,000 pounds a year from performance, 6 in 100 earned 30,000 or more, 71 in 100 worked outside the industry for 28
# weeks or more), SAG-AFTRA (about 160,000 members; about 87 in 100 earn under the 26,470-dollar health-plan threshold
# from acting), Actors' Equity Association annual report 2018-19 (51,938 members, 19,369 of them worked in the year,
# 2,259 new members; stage managers worked 55,423 work weeks, about 1,066 in an average week), the UK drama schools'
# figures (about 12,000 applicants for about 1,550 places a year at 22 accredited schools; about 700 to 1,000 acting
# graduates a year), NODA's 2002 survey of UK amateur theatre (437,800 taking part, 29 in 100 under 21, 25,760
# performances, 2,300 to 2,500 societies), AACT (about 7,000 US community theatres), NAYT's Youth Theatre Census 2024
# (over 100,000 young people in 414 youth theatres in England), Stagecoach (about 60,000 pupils a week), Cultural
# Learning Alliance (8,963 drama teachers in English secondary schools in 2019, 11,100 in 2010), Central Casting (about
# 200,000 registered background actors), the Directors Guild of America (19,673 members, 2026), WGA West (about 14,000
# members, 2026), the Writers' Guild of Great Britain (3,074 members, 2024), the Casting Society (nearly 1,200 members),
# TCG Theatre Facts 2019 (1,953 US nonprofit theatres, 21,000 productions, 38 million attendances), "That's
# Entertainment" (University of the West of Scotland, 2014: over 90,000 child performance licences a year in England,
# an estimate from a third of local authorities), and UK and US births (about 680,000 and 3.6 million a year).
# Everything else is an estimate, and says so. Real names stay in these comments and in PACK.md as sources: the moments
# never name a real person, production, theatre, studio, film, award, agency or union.

# Round 5, 2026-10-07: the outer world's keywords (chroma-engine/world-fields.md, W38 and W40): sector= on every career,
# institution= (an at: value) and standing= (0 an ordinary person, 1 local, 2 inside power, 3 national; chroma-world
# spec-7 section 2) on every career and summit.
TITLES = []
PERKS = []

# ---------------------------------------------------------------- careers: the actor's road
TITLES += [
  dict(name="professional actor", kind="career", sector="services", institution="employer", standing=0, ways="R B",
       profiles=[("R B", "Lives for the rush of a first night and the next big part, and goes after both hard."),
                 ("W G", "A company player: turns up word-perfect, serves the play and the people in it, and plays the "
                         "same theatres for years."),
                 ("U", "Studies the craft for life: the voice, the text, the body, and the truth of a scene.")],
       meets="need:meaning+.1 need:competence+.06 need:safety-.08 res:money-.05 res:time-.08",
       ages=(16, 100), share=.004,   # estimate from the union rolls: Equity UK 48,606 members (2024) against about
                                     # 680,000 UK births a year; Actors' Equity (US stage) 2,259 new members a year and
                                     # SAG-AFTRA about 160,000 members against 3.6 million US births; BLS counts 62,560
                                     # employed actors at a time (May 2023). Most work in few weeks of the year
       say="a professional actor",
       gained="'the showcase for agents' after [drama school student]; 'an open audition in the city' with [acting]; "
              "'opening night at the fringe' that turns into a run; 'the part that came with the letter'",
       lost="the work drying up for years, and the day job taking over ('the second job does not come'); 'leaving "
            "acting for another life'; 'burnout'",
       needs="[acting]; [drama school diploma], [union card] or [casting directory listing] in most of the trade; "
             "age 16 or more",
       turning="The agent rings with a good part in a tour of eight months, and the day job will not hold the place."),
  dict(name="voice actor", kind="career", sector="services", institution="media", standing=0, ways="U",
       profiles=[("U", "A craftsman of the voice: a hundred accents, perfect timing, the right breath for every line."),
                 ("R G", "Plays the dragon, the grandmother and the talking dog with the same joy, and the children "
                         "who listen know every one of them."),
                 ("W B", "A reliable voice for adverts, audiobooks and announcements: on time, on budget and always "
                         "in work.")],
       meets="need:competence+.06 need:autonomy+.06 res:time+.04 need:safety-.05",
       ages=(16, 100), share=.0005,   # estimate: voice-over, dubbing, animation, games and audiobook work as the main
                                      # living; many actors voice now and then without it being their career
       say="a voice actor",
       gained="'a voice for the cartoon' with [accents and voices]; years as a [professional actor] or [community-radio "
              "presenter]",
       lost="the voice going with age or illness; work moving to cheaper voices; 'leaving acting for another life'",
       needs="[accents and voices] or [acting]; [a showreel] (a voice reel) for most castings",
       turning="A games studio offers a year of steady work as a villain, and the scripts ask for things the voice "
               "may not survive."),
  dict(name="lead actor or actress", kind="career", sector="services", institution="media", standing=2, ways="R", refines="professional actor; voice actor",
       profiles=[("R", "Carries the show on raw presence, and the audience follows the fire."),
                 ("U B", "Builds the lead with care and plans the career around it, part by part."),
                 ("W G", "Leads the company as its first servant: first to arrive, last to leave, looking after "
                         "everyone on stage.")],
       meets="need:meaning+.08 need:competence+.06 res:money+.06 res:time-.12 res:health-.03",
       ages=(16, 100), share=.001,   # estimate: about 1 professional actor in 4 plays a lead in a paid production, a
                                     # film or a series at some point; most leads are in small companies and short runs
       say="playing the lead",
       gained="'the understudy goes on' as an [understudy]; 'the leading player leaves the company'; 'the part of a "
              "lifetime is cast'; 'a screen test'; 'the director calls again'; 'the lead voice in a series'; "
              "'opening night at the fringe' that transfers",
       lost="the run or the series ending, and the next part a smaller one; 'two actors, one part' lost; 'the reviews "
            "are in' and they are bad",
       needs="[professional actor] or [voice actor]; [acting]; most leads come to actors with [good notices], [an "
             "agent who believes in you] or [a director who keeps casting you]",
       turning="The producers want a star for the transfer, and the lead who made the show a hit may not go with it."),
  dict(name="director", kind="career", sector="services", institution="employer", standing=2, ways="U W",
       profiles=[("U W", "Serves the text: reads it until it gives up its meaning, and runs a fair, ordered rehearsal "
                         "room."),
                 ("R", "Makes bold, raw, surprising shows that set the room alight."),
                 ("B G", "Builds a body of work and a loyal company: the same actors and designers, show after show.")],
       meets="need:autonomy+.08 need:competence+.08 res:time-.12 need:safety-.04",
       ages=(20, 100), share=.001,   # estimate: BLS counts 154,470 producers and directors (US, 2023, most of them in
                                     # film, broadcast and television); the Directors Guild of America has 19,673
                                     # members (2026), the US stage directors' society 2,643 (2013)
       say="a director",
       gained="'a director is needed for the autumn play' with [directing actors]; years as a [professional actor], "
              "[stage manager], [community theatre director] or [drama teacher]; 'leaving acting for another life'",
       lost="a run of flops; the money moving on; 'burnout'",
       needs="[directing actors]; a first show that someone saw",
       turning="Three weeks into rehearsal the lead does not believe in the director's idea of the play, and says so "
               "in front of the company."),
  dict(name="playwright or screenwriter", kind="career", sector="services", institution="media", standing=1, ways="U R",
       profiles=[("U R", "Writes what has never been written, chasing a voice and an idea until the page burns."),
                 ("W G", "Writes the stories of a place and its people, so that they see themselves on stage."),
                 ("B", "Writes to sell: the pitch, the series and the deal, and a career built script by script.")],
       meets="need:meaning+.1 need:autonomy+.08 need:safety-.06 res:money-.03",
       ages=(18, 100), share=.0008,   # estimate: WGA West about 14,000 members (2026), the Writers' Guild of Great
                                      # Britain 3,074 (2024); counts those paid for a produced script at some point
       say="a playwright or screenwriter",
       gained="'the script competition' with [writing scripts]; 'the show you wrote to star in' and a fringe run; "
              "years as a [novelist], [journalist] or [professional actor]",
       lost="years without a production; a script bought and never made; a move back to novels or teaching",
       needs="[writing scripts] or [writing stories]; a first script someone staged",
       turning="The producers love the script and want the ending changed, the ending the whole play was written "
               "for."),
  dict(name="producer", kind="career", sector="services", institution="employer", standing=1, ways="B",
       profiles=[("B", "Raises the money, makes the deals and takes the risk, and means to win."),
                 ("W U", "Keeps the show on budget and on time, with contracts kept and everyone paid."),
                 ("R G", "Puts on the shows they love, for the people they love, and gambles the house on it.")],
       meets="need:autonomy+.08 res:money+.06 need:safety-.08 res:time-.12",
       ages=(20, 100), share=.0008,   # estimate: stage, film and television producers; BLS counts producers and
                                      # directors together (154,470, 2023)
       say="a producer",
       gained="'leaving acting for another life' with [striking a deal]; a show of their own that made money ([a "
              "company of your own]); years as a [stage manager], [director] or [talent agent]",
       lost="a flop that loses the money ('closing on Saturday'); the backers gone; 'burnout'",
       needs="[striking a deal] or [organising people]; money or people with money",
       turning="The show is losing money every night, and closing it means two hundred people out of work by "
               "Saturday."),
]

# ---------------------------------------------------------------- facets: the summit of a road (engine refines)
TITLES += [
  dict(name="artistic director", kind="career", sector="services", institution="employer", standing=2, ways="W B", refines="director",
       profiles=[("W B", "Runs the theatre as an institution: the season, the board, the budget and the duty to the "
                         "public."),
                 ("G", "Keeps a theatre for its town: its old audience, its local stories and the company that grew "
                       "up there."),
                 ("U R", "Turns the building into a laboratory for new work, and takes risks with the season.")],
       meets="need:meaning+.08 need:autonomy+.06 res:time-.15 res:ties+.04 need:safety-.03",
       ages=(25, 100), share=.0001,   # TCG Theatre Facts 2019: 1,953 US nonprofit theatres, each changing its
                                      # artistic director about every ten years (estimate), about 200 a year against
                                      # 3.6 million births; the UK rate is similar (estimate)
       say="artistic director of a theatre",
       gained="'the theatre needs an artistic director' after years as a [director]; a company of their own that "
              "grows a building",
       lost="the board choosing someone new; a season that empties the house; standing down after ten years",
       needs="[director] for years; [good notices] or [a company of your own]",
       turning="The board wants a season of safe old favourites to save the money, and the new writers were "
               "promised a stage."),
]

# ---------------------------------------------------------------- careers: side roads of the pathway
TITLES += [
  dict(name="stage manager", kind="career", sector="services", institution="employer", standing=0, ways="W U",
       profiles=[("W U", "Runs the show by the book, cue by cue, and knows where every prop and person is."),
                 ("G", "Looks after the company like a family: tea, plasters and calm on the worst nights."),
                 ("B R", "Thrives on the chaos of a fit-up and keeps a show going when everything breaks.")],
       meets="need:competence+.08 need:belonging+.05 res:time-.15 res:health-.03",
       ages=(17, 85), share=.001,   # Actors' Equity 2018-19: stage managers worked 55,423 work weeks, about 1,066 in an
                                    # average week (US stage); with touring, opera, television floor managers and the
                                    # UK, estimate
       say="a stage manager",
       gained="'the stage management team is a person short' with [stagecraft]; years as a [stage technician] or a "
              "[drama school student] on the technical course",
       lost="the hours; a move to production management or a [producer]; 'burnout'",
       needs="[stagecraft] or [calling the show]",
       turning="The lead is not in the building at the half, and the understudy has never had a rehearsal."),
  dict(name="casting director", kind="career", sector="services", institution="employer", standing=1, ways="W",
       profiles=[("W", "Gives every actor a fair hearing and the part to whoever is best for it."),
                 ("U B", "Knows every actor's work and every producer's need, and matches them shrewdly."),
                 ("R G", "Finds the raw talent nobody has seen: the street, the village hall, the school yard.")],
       meets="need:competence+.08 res:ties+.06 res:time-.1",
       ages=(20, 90), share=.0002,   # the Casting Society has nearly 1,200 members (US and abroad); with assistants
                                     # and the UK, estimate
       say="a casting director",
       gained="'leaving acting for another life' with [a casting eye]; years as an assistant to a casting office, or "
              "as a [talent agent] or [professional actor]",
       lost="the work drying up; a move to a [producer]",
       needs="[a casting eye]; [contact in the trade] helps",
       turning="The producers want a name for the lead, and the best audition all week came from an unknown."),
  dict(name="talent agent", kind="career", sector="services", institution="employer", standing=1, ways="B",
       profiles=[("B", "Drives a hard bargain for clients, and builds a list that makes money and names."),
                 ("W G", "Looks after a small list of actors for years, through the lean seasons too."),
                 ("U R", "Spots the strange, original talents early, and bets on them.")],
       meets="res:money+.06 res:ties+.08 res:time-.12 need:meaning-.02",
       ages=(20, 90), share=.0004,   # BLS: 12,870 agents and business managers of artists, performers and athletes
                                     # (May 2023); estimate for ever, with the UK
       say="a talent agent",
       gained="'leaving acting for another life' with [striking a deal] or [selling]; years as a [casting director] "
              "or an assistant in an agency",
       lost="the clients leaving for a bigger agency; a list that stops earning",
       needs="[striking a deal] or [selling]; [contact in the trade]",
       turning="The agency's best-paid client wants a part that one of its young clients was about to get."),
  dict(name="drama teacher", kind="career", sector="public", institution="school", standing=0, ways="U",
       profiles=[("U", "Teaches the craft: voice, text and movement, step by step."),
                 ("R G", "Gives shy children a voice and a stage, and builds a company of them."),
                 ("W B", "Runs the school play like a professional: discipline, results and a place at drama school for "
                         "the best.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.08 res:money+.02",
       ages=(20, 85), share=.002,   # Cultural Learning Alliance: 8,963 drama teachers in English secondary schools
                                    # (2019 headcount; 11,100 in 2010); private stage schools (one chain teaches about
                                    # 60,000 pupils a week) and youth theatres; estimate for ever
       say="a drama teacher",
       gained="a [teacher] with [acting] who takes the drama classes; 'leaving acting for another life' as a "
              "[professional actor]; years as a [community theatre director]",
       lost="drama cut from the timetable; a move to head of department or back to acting",
       needs="[acting] or [directing actors]; [teaching] or [cleared to work with children]; [graduate] and "
             "[professional registration] in state schools",
       turning="The head wants the drama hours for exam classes, and the school play is the only thing some children "
               "come in for."),
]

# ---------------------------------------------------------------- community: acting as a pastime, and the extra
TITLES += [
  dict(name="background artist", kind="community", ways="G",
       profiles=[("G", "Turns up early for the film shot in town and loves being part of it, a face in the crowd of "
                       "the place they live."),
                 ("W B", "Takes the day rate seriously: on time, in costume and invisible, call after call."),
                 ("U R", "Watches how films are made from the back of the crowd, and dreams of a line.")],
       meets="res:money+.02 need:belonging+.02 res:time-.04",
       ages=(16, 95), share=.008,   # Central Casting: about 200,000 registered background actors (US); most do a few
                                    # days and stop; estimate for ever
       say="works as an extra",
       gained="'extras wanted for a film in town'; [casting directory listing]",
       lost="the calls stopping; no time off the day job",
       needs="age 16 or more; a free day at short notice",
       turning="The director points at the extra by the bar and says: you, say this line."),
  dict(name="amateur actor", kind="community", ways="R G",
       profiles=[("R G", "Acts for the love of it with the same group of friends, year after year, in the village "
                         "hall."),
                 ("W", "Serves the society: learns the lines, sells the tickets and paints the set."),
                 ("U B", "Takes the craft seriously, and wants the best parts and the best review in the local "
                         "paper.")],
       meets="need:belonging+.08 need:meaning+.05 res:time-.06",
       ages=(14, 100), share=.04,   # NODA 2002: 437,800 taking part in UK amateur theatre (29 in 100 under 21) in
                                    # 2,300 to 2,500 societies; AACT: about 7,000 US community theatres; estimate for
                                    # ever
       say="an amateur actor",
       gained="'the local players need a cast'; years as a [youth theatre member]; 'never too late for the stage'; "
              "'the part you never got to play'",
       lost="no time for rehearsals any more; moving away; a quarrel at the society",
       needs="age 14 or more; an evening a week, more in show week",
       turning="The society's director casts a newcomer in the part everyone thought was yours."),
  dict(name="youth theatre member", kind="community", ways="R G",
       profiles=[("R G", "Plays for the fun of it with friends: costumes, games and the summer show."),
                 ("W", "Comes every week, learns every line and helps the younger ones."),
                 ("U B", "Works at it and wants the lead, a place at drama school and maybe more.")],
       meets="need:belonging+.08 need:competence+.05 res:time-.04",
       ages=(6, 21), share=.08,   # NAYT Youth Theatre Census 2024: over 100,000 young people in 414 youth theatres in
                                  # England; stage schools teach about 60,000 more a week in one chain alone; most stay
                                  # two or three years; estimate for ever
       say="in the youth theatre",
       gained="'a flyer for the youth theatre'; 'auditions for the school production'; a parent who signs them up",
       lost="growing out of it; exams; a move away",
       needs="a parent or carer who brings them, and the fees or a free place",
       turning="The summer show's lead goes to the new child, and the old hands are angry on your behalf."),
  dict(name="community theatre director", kind="community", ways="G W",
       profiles=[("G W", "Keeps the town's theatre going for everyone: the pantomime, the summer play and the people "
                         "who need it."),
                 ("R", "Puts on bold, mad shows in the church hall, and makes amateurs brave."),
                 ("U B", "Runs the society like a small professional company, and wins the drama festival.")],
       meets="need:meaning+.06 need:belonging+.06 res:time-.08 res:ties+.04",
       ages=(18, 100), share=.003,   # estimate: 2,300 to 2,500 UK amateur societies (NODA 2002) and about 7,000 US
                                     # community theatres (AACT), each with several directors over the years
       say="directs the local players",
       gained="'a director is needed for the autumn play' after years as an [amateur actor]; a [drama teacher] who "
              "runs the town society",
       lost="handing on at the annual meeting; a show that splits the society; moving away",
       needs="[amateur actor] for years, or [directing actors]",
       turning="The society's oldest member wants the lead again, and can no longer remember the lines."),
]

# ---------------------------------------------------------------- statuses: training, and the part held in reserve
TITLES += [
  dict(name="drama school student", kind="status", ways="", lasts=3,
       meets="need:competence+.08 need:meaning+.06 res:money-.08 res:time-.12 need:safety-.04",
       ages=(16, 40), share=.003,   # about 12,000 applicants for about 1,550 places a year at 22 accredited UK drama
                                    # schools (about 1 life in 440); with other acting degrees, estimate
       say="at drama school",
       gained="'drama school auditions' passed; a [scholarship] or [savings] for the fees",
       lost="three years over (the course ends with [drama school diploma]); leaving early",
       needs="[acting]; an audition passed; the fees, a loan or a [scholarship]",
       turning="The voice teacher says the accent from home has to go, and it is the voice of your family."),
  dict(name="understudy", kind="status", ways="", lasts=1,
       meets="need:competence+.04 need:autonomy-.05 need:safety-.03",
       ages=(16, 100), share=.0015,   # estimate: big musicals and long runs cover every lead; about 1 professional
                                      # actor in 3 understudies at some point
       say="understudying the lead",
       gained="'cast as understudy to the lead' as a [professional actor]",
       lost="the run ending; 'the understudy goes on' and takes the part",
       needs="[professional actor]; [learning lines]"),
]

# ---------------------------------------------------------------- perks: skills
PERKS += [
  dict(name="acting", kind="skill", ways="R U", odds=.05, skill_half=10, retires=None,
       ages=(6, 110), share=.06,   # estimate: youth theatres, school productions, amateur societies and drama schools
       say="can act",
       gained="'the school play' and years in a youth theatre or an amateur society; [drama school student]",
       lost="years off the stage", needs="nothing but nerve; a stage"),
  dict(name="screen acting", kind="skill", ways="U B", odds=.05, skill_half=8, retires=None,
       ages=(10, 110), share=.003,   # estimate
       say="knows how to act for the camera",
       gained="screen work as a [professional actor]; years as a [background artist]; 'a screen test'",
       lost="years away from the camera", needs="[acting]"),
  dict(name="improvisation", kind="skill", ways="R G", odds=.05, skill_half=8, retires=None,
       ages=(8, 110), share=.01,   # estimate: youth theatre and drama school games, improv groups
       say="can make a scene up on the spot",
       gained="weeks of games in a youth theatre; [drama school student]; 'the show you wrote to star in'",
       lost="years without a scene partner", needs="[acting] helps"),
  dict(name="stage combat", kind="skill", ways="R W", odds=.04, skill_half=6, retires=None,
       ages=(14, 90), share=.002,   # estimate: drama school courses and fight certificates
       say="can fight on stage without hurting anyone",
       gained="[drama school student]; a [professional actor] with [boxing or martial arts]",
       lost="years without a fight call", needs="[acting]; a body up to it"),
  dict(name="accents and voices", kind="skill", ways="U", odds=.05, skill_half=10, retires=None,
       ages=(10, 110), share=.003,   # estimate
       say="can do any accent and a hundred voices",
       gained="[drama school student]; years as a [voice actor]; an ear trained by a [second language]",
       lost="years of silence", needs="[acting] or [second language]"),
  dict(name="learning lines", kind="skill", ways="W", odds=.04, skill_half=8, retires=None,
       ages=(8, 110), share=.02,   # estimate
       say="learns lines fast and keeps them",
       gained="show after show as an [amateur actor] or [professional actor]; a season as an [understudy]",
       lost="years without a script", needs="[acting]"),
  dict(name="auditioning", kind="skill", ways="B R", odds=.05, skill_half=4, retires=None,
       ages=(10, 110), share=.01,   # estimate
       say="walks into an audition and owns the room",
       gained="audition after audition as a [professional actor] or [drama school student]; 'drama school "
              "auditions'; 'an open audition in the city'",
       lost="years without auditions", needs="[acting]"),
  dict(name="telling a story aloud", kind="skill", ways="G", odds=.05, skill_half=15, retires=None,
       ages=(8, 110), share=.02,   # estimate: storytellers, folk players, readers to children, radio
       say="can hold a room with a story",
       gained="years as a [drama teacher] or [community theatre director]; a grandparent who tells the old tales; "
              "the folk play at midwinter",
       lost="nobody left to tell", needs="[acting] or [public speaking] help"),
  dict(name="directing actors", kind="skill", ways="U G", odds=.05, skill_half=10, retires=None,
       ages=(16, 110), share=.004,   # estimate: professional, school and amateur directors
       say="can get the best out of a cast",
       gained="years as an [amateur actor] who takes the rehearsals; [drama teacher]; 'a director is needed for the "
              "autumn play'",
       lost="years without a rehearsal room", needs="[acting] or [stagecraft]"),
  dict(name="a casting eye", kind="skill", ways="U B", odds=.05, skill_half=6, retires=None,
       ages=(18, 110), share=.0005,   # estimate
       say="can see who is right for a part",
       gained="years as a [casting director], [talent agent], [director] or [producer]",
       lost="years away from the casting room", needs="[acting] or [directing actors]"),
  dict(name="writing scripts", kind="skill", ways="U W", odds=.05, skill_half=10, retires=None,
       ages=(12, 110), share=.002,   # estimate
       say="can write a script that plays",
       gained="[writing stories] put on a stage; 'the script competition'; 'the show you wrote to star in'",
       lost="years without a page", needs="[writing stories] or [acting]"),
  dict(name="calling the show", kind="skill", ways="W B", odds=.04, skill_half=6, retires=None,
       ages=(16, 110), share=.001,   # estimate: stage managers and deputies who call cues
       say="can call every cue of a show",
       gained="years as a [stage manager]; the prompt desk of an amateur society with [stagecraft]",
       lost="years away from the prompt desk", needs="[stagecraft]"),
]

# ---------------------------------------------------------------- perks: access (odds 0; they work through requires:)
PERKS += [
  dict(name="union card", kind="credential", ways="W G", odds=0, skill_half=None, retires=None,
       ages=(16, 110), share=.005,   # Equity UK 48,606 members (2024); SAG-AFTRA about 160,000; Actors' Equity (US
                                     # stage) 51,938 (2018-19); estimate for ever
       say="a member of the actors' union",
       gained="paid work as a [professional actor], [stage manager] or [voice actor]; years of work as a [background "
              "artist]",
       lost="letting the membership lapse after years out of the trade",
       needs="paid work in the trade"),
  dict(name="drama school diploma", kind="credential", ways="U W", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.0025,   # about 700 to 1,000 acting graduates a year from accredited UK schools, with
                                      # other acting degrees; estimate
       say="trained at drama school",
       gained="three years as a [drama school student]",
       lost="nothing: it stays",
       needs="[drama school student] to the end of the course"),
  dict(name="child performance licence", kind="credential", ways="W G", odds=0, skill_half=None, retires=16,
       ages=(3, 16), share=.015,   # "That's Entertainment" (UWS 2014): over 90,000 licences a year in England, many
                                   # for the same child; estimate for ever. Rules (UK guidance): a licensed chaperone,
                                   # three hours of schooling on a day missed, at most six days in a row, twelve hours
                                   # off overnight
       say="licensed to perform as a child",
       gained="'a casting call for children' won, with a parent who agrees; a youth theatre show with paid "
              "performances",
       lost="turning 16; a production over",
       needs="a parent or carer who agrees; a licensed chaperone; school hours kept"),
  dict(name="casting directory listing", kind="credential", ways="B R", odds=0, skill_half=None, retires=None,
       ages=(16, 110), share=.006,   # estimate: the actors' directory and the background agencies
       say="listed in the casting directory",
       gained="[drama school diploma]; work as a [professional actor] or [background artist]; the fee paid",
       lost="the fee unpaid; years out of the trade",
       needs="training or professional credits; the yearly fee"),
  dict(name="a fringe slot", kind="credential", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(16, 110), share=.003,   # the largest fringe festival had over 3,300 to 3,500 shows in 2024, most from
                                     # small companies; estimate for ever
       say="has a slot at the fringe",
       gained="'the show you wrote to star in'; [a company of your own], or a society that takes a show to the fringe",
       lost="the festival over",
       needs="a show and the venue fee; [writing scripts] or a company"),
]

# ---------------------------------------------------------------- perks: standing
PERKS += [
  dict(name="a lead role to remember", kind="standing", ways="R G", odds=.04, skill_half=20, retires=None,
       ages=(6, 110), share=.04,   # estimate: the lead in a school production, a youth theatre show, an amateur
                                   # society's play or a one-person show; the professional lead brings it too
       say="once played the lead, and people still talk about it",
       gained="'casting night at the local players'; 'the summer show casts its lead'; 'a casting call for children'; "
              "'opening night at the fringe'; [lead actor or actress]",
       lost="the town forgetting, after many years", needs="a stage and a part; [acting]"),
  dict(name="good notices", kind="standing", ways="U W", odds=.04, skill_half=5, retires=None,
       ages=(16, 110), share=.003,   # estimate
       say="has had good notices",
       gained="'the reviews are in' and kind; years as a [professional actor], [director] or [playwright or "
              "screenwriter]",
       lost="years without a review; a bad run", needs="work that critics see"),
  dict(name="a known face", kind="standing", ways="B R", odds=.05, skill_half=8, retires=None,
       ages=(10, 110), share=.002,   # estimate: actors in long-running series and adverts
       say="has a face people know from the screen",
       gained="a long run on screen as a [professional actor] with [screen acting]; 'a screen test' won",
       lost="years off the screen", needs="[screen acting]"),
  dict(name="an award for acting", kind="standing", ways="W B", odds=.04, skill_half=25, retires=None,
       ages=(10, 110), share=.002,   # estimate: national theatre and screen awards, and the best-actor awards of about
                                     # 100 amateur drama festivals (about 500 groups compete)
       say="has won an award for acting",
       gained="a best-actor award at a drama festival as an [amateur actor]; a national award as a [lead actor or "
              "actress]; 'the show is a hit'",
       lost="nothing: the award stays, though its glow fades", needs="[acting]; a part people saw"),
  dict(name="a cult following", kind="standing", ways="R G", odds=.05, skill_half=10, retires=None,
       ages=(14, 110), share=.0005,   # estimate
       say="has a small, devoted following",
       gained="a strange fringe show, a cult film or a voice in a series; [following online]",
       lost="the fans moving on", needs="a show or a part that a few people love"),
]

# ---------------------------------------------------------------- perks: bonds
PERKS += [
  dict(name="an agent who believes in you", kind="bond", ways="B G", odds=.05, skill_half=4, retires=None,
       ages=(10, 110), share=.003,   # estimate: an agent who pushes for the client, not just a name on a list
       say="has an agent who believes in them",
       gained="'the showcase for agents'; [good notices]; years with the same [talent agent]",
       lost="the agent retiring or leaving; years without work", needs="[professional actor] or a showcase"),
  dict(name="a director who keeps casting you", kind="bond", ways="U W", odds=.05, skill_half=5, retires=None,
       ages=(16, 110), share=.002,   # estimate
       say="has a director who keeps casting them",
       gained="'kept your word' in a rehearsal room; two shows with the same [director]",
       lost="a falling out; the director retiring", needs="[professional actor]"),
  dict(name="a company that feels like family", kind="bond", ways="G R", odds=.04, skill_half=6, retires=None,
       ages=(8, 110), share=.02,   # estimate: amateur societies, youth theatres, rep and touring companies
       say="belongs to a company that feels like family",
       gained="years in the same youth theatre, amateur society or rep company; 'made a friend' on the tour",
       lost="the company breaking up; moving away", needs="years with the same company"),
  dict(name="a year group from drama school", kind="bond", ways="R U", odds=.04, skill_half=10, retires=None,
       ages=(18, 110), share=.002,   # estimate: the classmates who pass on work and turn up on first nights
       say="has the year group from drama school",
       gained="three years as a [drama school student]", lost="years apart", needs="[drama school student]"),
  dict(name="a producer who backs you", kind="bond", ways="B", odds=.05, skill_half=4, retires=None,
       ages=(18, 110), share=.0005,   # estimate
       say="has a producer who backs them",
       gained="'the show is a hit'; [good notices] as a [lead actor or actress], [director] or [playwright or "
              "screenwriter]",
       lost="a flop together; the producer gone", needs="a show that made money"),
]

# ---------------------------------------------------------------- perks: assets
PERKS += [
  dict(name="a showreel", kind="asset", ways="B U", odds=0, skill_half=None, retires=None,
       ages=(14, 110), share=.004,   # estimate: a reel of screen work, or a voice reel
       say="has a showreel",
       gained="screen work as a [professional actor] or [background artist]; a voice reel as a [voice actor]",
       lost="the reel out of date after years", needs="screen or voice work to put on it"),
  dict(name="repeat fees", kind="asset", ways="B W", odds=0, skill_half=None, retires=None,
       ages=(10, 110), share=.001,   # estimate: residuals and repeat fees from screen and voice work
       say="earns repeat fees",
       gained="a long-running series, an advert or a voice that keeps airing; 'the lead voice in a series'",
       lost="the series off the air", needs="screen or voice work that is shown again"),
  dict(name="a company of your own", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(16, 110), share=.002,   # estimate: small touring and fringe companies, folk and street theatre troupes
       say="runs a theatre company of their own",
       gained="'the show you wrote to star in'; years as a [producer], [director] or [community theatre director]",
       lost="the money gone; the company broken up", needs="[writing scripts] or [directing actors]; a little money"),
]
