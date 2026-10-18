# ---------- career, the spheres' first jobs (item 15, stage 4; Library thread, 2026-10-09): one per sphere, each with
# sphere= and face= beside sector= (chroma-engine/notes/world-fields.md). Three more first jobs are existing titles
# tagged in place: waiter or bartender (gather.R), care worker (care.W), apprentice (prod.G).
TITLES += [
  dict(name="court clerk", kind="career", sector="public", sphere="rule", face="rule.W", ways="W U",
       meets="need:meaning+.05 need:safety+.05 res:money+.03 res:time-.1 need:autonomy-.03",
       ages=(18, 70), share=.006,   # estimate: court and tribunal staff are about 1 worker in 400 in a rich country;
                                    # many start young behind the bench and move on, so more hold it than hold it now
       say="a court clerk",
       gained="'a job interview' at the town's court after school or college, often as 'your first full-time job': a "
              "desk below the bench, the day's list and the files",
       lost="'a promotion is open' in the court office, a move into law, 'new technology changes your job', retirement",
       needs="[school-leaving certificate]; age 18 or more; a background check",
       turning="On a busy list day a claim from a man with no lawyer is missing a page, and the bench will strike it "
               "out at eleven. The clerk knows where the page went."),
  dict(name="session player", kind="career", sector="services", sphere="arts", face="arts.U", ways="U R",
       meets="need:competence+.08 need:autonomy+.05 need:safety-.05 res:money+.02 res:time-.1",
       ages=(16, 80), share=.003,   # estimate: a few people in 1,000 ever play for hire on other people's recordings
                                    # and shows, most for a few years beside other work
       say="a session player",
       gained="years of practice ('learned a skill'), then a studio short of a player the night before, and a name "
              "passed from one band to the next",
       lost="the calls drying up, a band of their own, 'new technology changes your job', a steadier job",
       needs="[musical instrument] played well, by ear and from the page",
       turning="Three hours are booked and the producer wants the part exactly as written. On the second take the "
               "player hears a better line in it."),
  dict(name="alms visitor", kind="career", sector="services", sphere="faith", face="faith.W", ways="W G",
       meets="need:meaning+.1 need:belonging+.05 res:money+.01 res:time-.08 res:ties+.03",
       ages=(16, 85), share=.004,   # estimate: a congregation's paid visitor for its alms fund, a few hours a week;
                                    # far more people visit unpaid ([neighbourhood volunteer], [deacon or elder])
       say="an alms visitor",
       gained="a few paid hours a week from the congregation's alms fund, after years of helping at the hall: a list of "
              "names, a bus pass and the week's bags of shopping",
       lost="the fund running dry, a full-time job elsewhere, the list handed on to a younger visitor",
       needs="[regular worshipper] or years of helping at the hall; a background check",
       turning="An old man on the visiting list has stopped opening his door, and the fund drops anyone not seen this "
               "month. The form is due on Friday."),
  # the sphere's job is "tutor for hire"; the modern name and the cast's role (spheres-data learn.json, learn.B) is
  # the private tutor
  dict(name="private tutor", kind="career", sector="knowledge", sphere="learn", face="learn.B", ways="B U R",
       meets="need:autonomy+.05 need:competence+.05 res:money+.03 res:time-.05",
       ages=(16, 80), share=.06,   # estimate: many students tutor younger pupils for pay for a while, and private
                                   # tuition is common in most rich countries; few make a living of it
       say="a private tutor",
       gained="a card on the library noticeboard or a word from a neighbour, and a first pupil at a kitchen table, "
              "often while still a student",
       lost="a full-time job, the exam season ending, the families finding a cheaper tutor online",
       needs="good marks in the subject; [school-leaving certificate] helps",
       turning="A parent paying double asks the tutor to write the coursework their child is meant to write. The rent "
               "is due on Friday."),
  dict(name="market porter", kind="career", sector="services", sphere="comm", face="comm.W", ways="W B G",
       meets="need:belonging+.05 need:competence+.03 res:money+.03 res:time-.1 res:health-.05",
       ages=(16, 65), share=.01,   # estimate: wholesale and street markets take on porters, loaders and stall hands,
                                   # a first job for some young people in market towns and cities
       say="a market porter",
       gained="turning up at the wholesale market before dawn and being picked for a barrow, or a cousin already on "
              "the stalls who puts in a word; often 'your first real job'",
       lost="a bad back, the market moving out of town, a stall of their own",
       needs="age 16 or more; fitness; a start at four in the morning",
       turning="Wheeling a crate to a stall, the porter sees that the trader's scale has been set light. Both the "
               "trader and the buyer tip the porter every week."),
  dict(name="door staff", kind="career", sector="services", sphere="prot", face="prot.B", ways="B R",
       meets="need:competence+.03 need:safety-.03 res:money+.05 res:time-.1 res:health-.05",
       ages=(18, 60), share=.016,   # estimate: door and event security take on a few young adults in 100 for a while,
                                    # most of them men, many for a year or two beside study or a day job
       say="one of the door staff",
       gained="a short licence course and a first Friday on the door of a bar or club, often through a friend already "
              "on the door",
       lost="the licence lapsing, the venue closing, the nights wearing them down, a move to guarding by day "
            "([security guard])",
       needs="age 18 or more; the door licence; a clean record in most places",
       turning="Near closing a young customer is too drunk to stand, and the friends who came with them have gone. "
               "The rule is to put them outside the door."),
]

