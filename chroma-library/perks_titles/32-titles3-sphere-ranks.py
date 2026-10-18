# ---------- the spheres' titles at two ranks (item 15, stage 4; Library thread, 2026-10-09): the 28 gaps of
# chroma-packs/spheres/title-gaps.md, with Packs' faces, ranks, kinds, sectors, ways, ages and shares. Given only with
# the Engine's sph_titles on (off until the refit).
TITLES += [
  dict(name="lay judge", kind="community", sphere="rule", face="rule.W", ways="W U",
       meets="need:meaning+.08 need:competence+.03 res:ties+.03 res:time-.08",
       ages=(25, 75), share=.003,   # estimate: lay judges and lay magistrates sit in several legal systems, about 1
                                    # adult in 3,000 at a time, in terms of some years; a few in 1,000 ever sit
       say="a lay judge",
       gained="an application and an interview after years as a [court clerk] or a [community-mediation volunteer], "
              "or a name put forward by people who know them ([good name in town]); training, then a first sitting "
              "beside two others on the bench, unpaid",
       lost="the term ending, the age limit, a move ('moved away'), a conflict of interest, a record of their own",
       needs="age 25 or more; years at the court, a mediation service, or [good name in town]; not "
             "[someone with a record]",
       turning="A young mother stands before the bench for a fine she could not pay, now doubled. The two others on "
               "the bench want to get through the list by lunch."),
  dict(name="paralegal", kind="career", sector="knowledge", sphere="rule", face="rule.U", ways="U W",
       meets="need:competence+.05 need:safety+.03 res:money+.04 res:time-.1 need:autonomy-.03",
       ages=(18, 70), share=.006,   # estimate: the US counts about 350,000 paralegals and legal assistants (BLS);
                                    # many hold the post for a few years on the way into law or out of it
       say="a paralegal",
       gained="'a job interview' at a law firm or an advice centre after school or college, often as 'your first "
              "full-time job': the files, the forms and the deadlines",
       lost="the exams and a move up to [lawyer], 'new technology changes your job', 'a wave of layoffs at work'",
       needs="[school-leaving certificate]; a short legal course in many places",
       turning="A family's appeal against eviction must reach the tribunal by four tomorrow, and the lawyer who should "
               "sign it is away. The finished form is on the paralegal's desk."),
  dict(name="lawyer", kind="career", sector="knowledge", sphere="rule", face="rule.U", ways="U B",
       profiles=[("U B", "Knows the law to the letter and uses every rule in it for the client."),
                 ("R", "Fights in court for the clients nobody else will take, and says what they think of the "
                       "rules.")],
       meets="need:competence+.08 need:autonomy+.03 res:money+.1 res:time-.15 res:health-.03",
       ages=(23, 80), share=.006,   # estimate: the US counts about 800,000 lawyers in a workforce near 160 million
                                    # (BLS); long careers and few leavers keep the lifetime share near the share at work
       say="a lawyer",
       gained="a law degree ([graduate]), the professional exams and a training post ([professional registration]); "
              "or years as a [paralegal], evening study and the same exams",
       lost="retirement, being struck off (the knowledge stays), a move onto the bench or into a firm's own office, "
            "'burnout'",
       needs="[graduate] and [professional registration]; or years as a [paralegal] and the exams",
       turning="The firm's best client swears a contract was lost years ago. In the client's own old file is a copy "
               "that would sink their case."),
  dict(name="mediator", kind="career", sector="services", sphere="rule", face="rule.G", ways="G W",
       meets="need:meaning+.08 need:competence+.05 need:safety-.03 res:money+.03 res:time-.08",
       ages=(25, 80), share=.0005,   # estimate: paid mediators of family, workplace and business disputes are a few
                                     # workers in 10,000; most come to it late, from law, care work or volunteering
       say="a mediator",
       gained="years as a [community-mediation volunteer], or a career in law or care and the course for "
              "[mediation accreditation]; then a first paid case from a court's list or a family service",
       lost="the cases drying up, a service's contract going elsewhere, retirement",
       needs="[mediation accreditation]; [settling disputes] helps; age 25 or more",
       turning="Two partners, friends since school, are splitting up their building firm, and each wants the van, the "
               "name and the customers. Their families are waiting outside the room."),
  dict(name="community centre manager", kind="career", sector="public", sphere="gather", face="gather.W", ways="W G",
       profiles=[("W G", "Keeps the doors open to everyone, the rota fair and the lunch club fed."),
                 ("U B", "Keeps the centre alive on grants won, a careful budget and the right friends at the "
                         "council.")],
       meets="need:meaning+.1 need:belonging+.05 res:money+.03 res:time-.1 res:health-.03",
       ages=(21, 70), share=.002,   # estimate: a town of 50,000 has a handful of community centres with one paid
                                    # manager each; few hold the post, and many hold it for years
       say="the community centre's manager",
       gained="years on the rota as a [community-kitchen volunteer] or a [neighbourhood volunteer], or the books as a "
              "[club treasurer], then 'a job interview' when the old manager retires",
       lost="the council's grant cut, the building sold, 'burnout', retirement",
       needs="years volunteering in the neighbourhood; [organising people] or [bookkeeping] helps; a background check",
       turning="The council offers a year's grant if every group pays for its room. The pensioners' tea and the youth "
               "night have always met for free."),
  dict(name="events promoter", kind="career", sector="services", sphere="gather", face="gather.B", ways="B R",
       meets="need:autonomy+.05 need:competence+.03 need:safety-.05 res:money+.03 res:time-.12 res:health-.03",
       ages=(18, 70), share=.002,   # estimate: the US counts about 140,000 meeting and event planners (BLS); with
                                    # club and concert promoters, many promoting for a few years beside another job
       say="an events promoter",
       gained="years behind the bar as a [waiter or bartender], the books as a [club treasurer] or a committee as a "
              "[festival organiser], then a first night of their own in a rented room, sold through friends",
       lost="a night that loses money, the venue closing, 'burnout', a steadier job",
       needs="age 18 or more; contacts ([name on the local scene] or [contact in the trade]); money up front "
             "([savings])",
       turning="Two days before the big night half the tickets are unsold, and the headline act's agent wants the rest "
               "of the fee now."),
  dict(name="DJ", kind="career", sector="services", sphere="gather", face="gather.R", ways="R B",
       profiles=[("R B", "Reads the room, keeps the floor moving until the lights come up, and makes the name fill "
                         "it."),
                 ("G", "Plays the town's weddings, birthdays and yearly dances, and knows which old song brings the "
                       "grandparents up.")],
       meets="need:autonomy+.05 need:belonging+.05 need:safety-.05 res:money+.02 res:time-.1 res:health-.05",
       ages=(16, 65), share=.001,   # estimate: about 1 person in 1,000 ever plays records for pay, most for a few
                                    # years beside other work; at 16 the paid nights are birthdays and school dances
       say="a DJ",
       gained="records collected for years, borrowed decks and an early slot on a quiet night, often after nights as "
              "a [waiter or bartender] or years as an [amateur band member]; [sound mixing] helps",
       lost="the bookings drying up, the late nights wearing them down, the club closing, a day job",
       needs="[sound mixing] or a good ear, a collection and the gear (often [savings]); age 18 or more for bars and "
             "clubs",
       turning="The floor is full at one in the morning, and the owner wants the music down for the neighbours. The "
               "crowd wants one more song."),
  dict(name="café or bar owner", kind="career", sector="services", sphere="gather", face="gather.G", ways="G B",
       profiles=[("G B", "Keeps the corner place where the same faces meet every morning, and makes it pay."),
                 ("W", "Runs a room where no one is turned away: the cheap soup, the lonely regular never rushed.")],
       meets="need:belonging+.08 need:autonomy+.08 res:money+.02 res:time-.12 res:health-.03",
       ages=(21, 80), share=.004,   # estimate: owners and keepers of small cafés, bars and pubs; most such places are
                                    # small firms, and many change hands within a few years, so more hold it than now
       say="a café owner",
       gained="years behind someone else's counter as a [waiter or bartender] or [cook], or a [shop owner] who turns "
              "the front of the shop into tables; [savings] or the [family business] pay for the lease, and a sign "
              "goes up with their name on it",
       lost="the rent rising past the takings, a buyer for the lease, 'burnout', the street changing round it, "
            "retirement",
       needs="[waiter or bartender], [cook] or [shop owner] first; [savings] or [family business]; age 21 or more; "
             "[food hygiene certificate], and [drinks licence] for a bar",
       turning="The old regular who has had the window table every morning for twenty years now sits there all day "
               "over one cup of tea, and a queue is waiting at the door."),
  dict(name="music teacher", kind="career", sector="knowledge", sphere="arts", face="arts.U", ways="U W",
       profiles=[("U W", "Teaches scales, reading and patience, and writes down every pupil's progress."),
                 ("R G", "Teaches by ear and by playing along, the old tunes first, and the pupils play in the town "
                         "band.")],
       meets="need:competence+.08 need:meaning+.05 res:money+.02 res:time-.08",
       ages=(18, 80), share=.002,   # estimate from US BLS counts of musicians and of arts teachers, with the turnover of
                                    # part-time teaching; many teach beside playing, in schools or at home
       say="a music teacher",
       gained="a [session player] or [amateur band member] who takes a first pupil for a little money, then a card in "
              "the library window and a waiting list; some through a music college and a post in a school",
       lost="the pupils moving on, a full-time school post, stiffening hands, retirement",
       needs="[musical instrument] played well; [teaching] helps; [cleared to work with children] for children's "
             "lessons",
       turning="A pupil who has practised every day for a year still cannot keep the beat, and the parents ask "
               "whether another term is worth it."),
  dict(name="touring musician", kind="career", sector="services", sphere="arts", face="arts.R", ways="R B",
       profiles=[("R B", "Lives for the night's show and the next town, and fights for a bigger stage."),
                 ("U B", "Tunes the set night by night, reads every contract, and knows each venue's sound.")],
       meets="need:autonomy+.08 need:competence+.05 res:money-.02 res:time-.12 res:health-.05 res:ties-.05",
       ages=(17, 70), share=.002,   # estimate from US BLS counts of musicians and singers; most who tour do it for a
                                    # few years in their twenties, often for little money
       say="a touring musician",
       gained="an [amateur band member] whose band gets its first run of dates out of town, or a [session player] "
              "hired for a singer's tour; a van, a borrowed amplifier and a list of venues",
       lost="the band splitting, the money running out, a child at home, the body tiring of the road, a steady job",
       needs="[musical instrument] or [singing] good enough for a paying crowd; age 17 or more, and 18 for the bars "
             "on most tours",
       turning="On the fourth night of the tour the venue pays half the agreed fee, and the band needs fuel to reach "
               "the next town."),
  dict(name="folk musician", kind="community", sphere="arts", face="arts.G", ways="G R",
       profiles=[("G R", "Plays the old tunes with friends in the corner of the pub until late."),
                 ("W", "Plays at every wedding, wake and benefit night the town holds, for the town.")],
       meets="need:belonging+.08 need:meaning+.05 res:ties+.03 res:time-.05",
       ages=(12, 95), share=.02,   # estimate: folk sessions, dance bands and singing circles meet in most towns; a
                                   # couple of people in 100 play in one for some years
       say="a folk musician",
       gained="sitting in at a session in the back room of a pub or at a festival, learning the tunes by ear from "
              "older players, and being asked back",
       lost="moving away, the session ending when its oldest players die, other music, stiffening hands",
       needs="none; [musical instrument] or [singing]",
       turning="The session's oldest player plays a slow tune nobody else knows, and says it was their mother's and "
               "has never been written down."),
  dict(name="craft maker", kind="career", sector="industry", sphere="arts", face="arts.G", ways="G U",
       profiles=[("G U", "Makes things the old way, by hand, and learns the material for a lifetime."),
                 ("B R", "Sells hard at fairs and markets, and makes a name with bold work.")],
       meets="need:competence+.08 need:autonomy+.08 res:money-.02 res:time-.08",
       ages=(18, 90), share=.005,   # estimate: potters, weavers, woodworkers, jewellers and other makers who earn part
                                    # of a living from what they make; most beside another job
       say="a craft maker",
       gained="a folk musician, an [apprentice] or [carpenter] who starts selling what they make at fairs and markets, "
              "or a [workshop] at home and a first table at the craft fair",
       lost="the stall not paying, cheap copies, hands or eyes failing, a steady job",
       needs="a craft learned by hand ('learned a skill'); [workshop] or [tools of one's own]",
       turning="A shop in the city offers to sell the maker's bowls, if they can be made faster and cheaper with a "
               "machine for the hard part."),
  dict(name="independent preacher", kind="faith", sphere="faith", face="faith.B", ways="B R",
       profiles=[("B R", "Builds a hall of their own by force of voice, and the followers choose to come."),
                 ("U W", "Preaches careful readings of the texts, and keeps the hall's books open to every member.")],
       meets="need:meaning+.1 need:autonomy+.08 res:money-.02 res:time-.1 res:ties+.03",
       ages=(21, 90), share=.002,   # estimate: preachers who lead a congregation of their own outside any wider body; a
                                    # few in 1,000 believers, most for small gatherings in hired rooms
       say="a preacher with a hall of their own",
       gained="a [convert], [regular worshipper] or [street preacher] whose small following hires a room on the day "
              "of worship, then a lease on an old shop or hall with their name on the board",
       lost="the following drifting away, a split in the hall, the lease lost, the hall handed to a successor, a "
            "scandal",
       needs="[convert], [regular worshipper] or [street preacher] first; age 21 or more; [public speaking] and "
             "[scripture] help",
       turning="The hall's biggest giver, who pays most of the rent, asks for a seat at the front and a say in next "
               "month's sermons."),
  dict(name="complementary therapist", kind="career", sector="services", sphere="care", face="care.B", ways="B G",
       profiles=[("B G", "Runs a small practice of their own: a calm room and hands-on care that clients choose for "
                         "themselves."),
                 ("U", "Keeps careful notes, says plainly what the sessions can and cannot do, and sends clients on "
                       "to a doctor.")],
       meets="need:autonomy+.08 need:meaning+.05 res:money+.01 res:time-.08",
       ages=(18, 75), share=.005,   # estimate from US BLS counts of massage therapists, with others in massage,
                                    # reflexology and aromatherapy; many work part time and for a few years
       say="a complementary therapist",
       gained="a short course in massage or another hands-on therapy, a folding table and a room rented by the hour, "
              "then clients who come back",
       lost="too few clients, the room's rent, hands or back wearing out, a move into nursing or physiotherapy",
       needs="none; a short course, and insurance to practise",
       turning="A regular client with back pain mentions a new numbness down one leg, and says she would rather keep "
               "seeing the therapist than go to her doctor."),
  dict(name="physiotherapist", kind="career", sector="knowledge", sphere="care", face="care.B", ways="B U",
       profiles=[("B U", "Builds a name and a list of patients who ask for them, and backs every plan with measured "
                         "progress."),
                 ("R W", "Gets people moving again fast, cheers them through every exercise, and gives every patient "
                         "on the ward the same."),
                 ("G", "Lets the body mend at its own pace, with patient exercises done at home among family.")],
       meets="need:competence+.08 need:meaning+.05 res:money+.05 res:time-.1",
       ages=(22, 70), share=.002,   # estimate: physical therapists are about 1 worker in 600 in the US (BLS), most
                                    # of them for a whole career, with some leaving for other health work
       say="a physiotherapist",
       gained="a physiotherapy degree ([graduate]) and the [professional registration], then 'a job interview' and "
              "'your first full-time job' on a hospital's wards; later, often, a practice of their own",
       lost="retirement, a bad back of their own, 'burnout', or being struck off (the skill stays)",
       needs="[graduate] in physiotherapy and [professional registration]",
       turning="A semi-professional player asks the physiotherapist to sign him fit for the cup final. His knee is "
               "two weeks from ready."),
  dict(name="hospice volunteer", kind="community", sphere="care", face="care.G", ways="G W",
       profiles=[("G W", "Sits with the dying and their families, and keeps the rota so no one is left alone."),
                 ("R", "Brings music, news and laughter onto the ward, and keeps birthdays for those who will not "
                       "see another.")],
       meets="need:meaning+.1 need:belonging+.05 res:time-.05 res:ties+.03",
       ages=(16, 90), share=.02,   # estimate: hospices lean on volunteers, often several for each paid post, and many
                                   # serve for a few years, often after a death in their own family
       say="a hospice volunteer",
       gained="a training evening at the local hospice, often after losing someone there or through a friend on the "
              "rota; then a shift a week at the tea trolley or the bedside",
       lost="stepping back after a hard year, a move, 'burnout', age",
       needs="none; the hospice's short training and a background check; age 16 or more",
       turning="A dying man asks the volunteer to write a letter to the daughter he has not spoken to in twenty "
               "years. Volunteers are told to keep out of family matters."),
  dict(name="teaching assistant", kind="career", sector="public", sphere="learn", face="learn.W", ways="W G",
       profiles=[("W G", "Makes sure the slowest reader and the child at the back get the same help as the rest."),
                 ("B", "Takes the post as the first step to a teacher's job, and studies for it at night.")],
       meets="need:meaning+.08 need:belonging+.05 res:money+.02 res:time-.08",
       ages=(17, 70), share=.03,   # estimate: the US counts about 1.3 million teaching assistants (BLS); many parents
                                   # take the post while their own children are at school, and turnover is high
       say="a teaching assistant",
       gained="'a job interview' at a local school, often after years of helping in class as a parent; the checks, "
              "a lanyard and a reading group of six",
       lost="the school's budget cut, teacher training ([teacher]), 'a new job at last' with better pay",
       needs="[cleared to work with children]; age 17 or more",
       turning="A quiet girl in the reading group copies every word from her neighbour's book. The assistant begins "
               "to think she cannot see the board."),
  dict(name="consultant", kind="career", sector="knowledge", sphere="learn", face="learn.B", ways="B U",
       profiles=[("B U", "Sells expert advice by the day, and guards the know-how that sets the price."),
                 ("W", "Writes the standards and checks a whole trade then keeps, and signs only what is true.")],
       meets="need:competence+.05 need:autonomy+.05 res:money+.1 res:time-.12",
       ages=(23, 75), share=.01,   # estimate: management analysts and other advisers are about 1 worker in 160 in the
                                   # US (BLS); many hold the title for some years mid-career
       say="a consultant",
       gained="years as a [private tutor], [teacher], [accountant] or [data analyst], then a firm that sells advice "
              "by the day, or a first client of one's own",
       lost="the contracts drying up, a post on a client's own staff, retirement",
       needs="[graduate]; years of trusted know-how in one field",
       turning="A client pays for a review of its offices and has already decided to close half of them. It wants "
               "the report to say so."),
  dict(name="mechanic", kind="career", sector="industry", sphere="learn", face="learn.R", ways="R U",
       profiles=[("R U", "Learns each engine by taking it apart, and finds the fault by feel and by testing."),
                 ("B", "Runs a garage of their own, prices the job, and builds a name across town.")],
       meets="need:competence+.08 need:autonomy+.03 res:money+.05 res:time-.1 res:health-.03",
       ages=(16, 75), share=.01,   # estimate: automotive technicians are about 1 worker in 200 in the US (BLS); many
                                   # start young in a garage and move to other trades later
       say="a mechanic",
       gained="an [apprentice]'s years in a garage, Saturdays as a [repair-cafe volunteer], or [car mechanics] "
              "learned at home; then 'your first full-time job' under a car",
       lost="a bad back, the garage closing, 'new technology changes your job' as the engines change, retirement",
       needs="[car mechanics] or an apprenticeship; age 16 or more",
       turning="An old customer's car fails on its brakes. She cannot pay for the work this month and asks the "
               "mechanic to pass it anyway."),
  dict(name="community language teacher", kind="community", sphere="learn", face="learn.G", ways="G U",
       profiles=[("G U", "Keeps the home tongue alive through the old songs and stories, and the careful grammar "
                         "behind them."),
                 ("W R", "Opens the class to every child who comes, and keeps it loud with games and songs.")],
       meets="need:belonging+.08 need:meaning+.08 res:time-.05 res:ties+.05",
       ages=(15, 90), share=.005,   # estimate: weekend and evening schools of a home tongue are common wherever
                                    # families have moved from elsewhere; a few in each such community teach
       say="a teacher of the home tongue",
       gained="a few children of family friends at a kitchen table, then a borrowed classroom or hall on rest days, "
              "often while still at school or college",
       lost="the families moving away, the children growing up, the hall lost, age",
       needs="[second language] spoken well, often from home",
       turning="In front of the class, a grandmother says the textbook's word for bread is wrong. In her village it "
               "was another word."),
  dict(name="outdoor instructor", kind="career", sector="services", sphere="learn", face="learn.G", ways="G R",
       profiles=[("G R", "Teaches the woods, the hills and the river by doing, and loves a wild day out."),
                 ("U", "Reads the weather, the map and the water, and teaches the method of coming home safe.")],
       meets="need:competence+.05 need:autonomy+.05 res:health+.05 res:money+.02 res:time-.1",
       ages=(18, 65), share=.002,   # estimate: outdoor centres hire a few instructors each, many for a few seasons
                                    # in their twenties before a steadier job
       say="an outdoor instructor",
       gained="years as a [scout or guide], a [youth coach] or a [search-and-rescue volunteer], or [knowing the "
              "woods] from childhood; then the instructor's tickets and a first season at an outdoor centre",
       lost="a bad knee, the season ending, the centre closing, a steadier job in town",
       needs="[knowing the woods] or years out of doors; [cleared to work with children]; first aid and the "
             "centre's own tickets; age 18 or more",
       turning="The river is rising on the morning a school group comes for its canoe day. The teacher says the "
               "coach is booked and the children have waited all term."),
  dict(name="quality inspector", kind="career", sector="industry", sphere="prod", face="prod.U", ways="U W",
       profiles=[("U W", "Measures every sample to the drawing, and finds the fault before the customer does."),
                 ("R B", "Works the line at speed, knows which faults matter, and keeps the shift's output moving.")],
       meets="need:competence+.05 need:safety+.03 res:money+.03 res:time-.1 need:belonging-.02",
       ages=(17, 70), share=.01,   # estimate (Packs): US BLS counts about half a million inspectors, testers and
                                   # samplers; many move to the post from the line for a few years
       say="a quality inspector",
       gained="a move off the line after years as [factory worker], or 'a job interview' for the test bench at the end "
              "of the line: a gauge, a drawing and the right to stop a batch",
       lost="'new technology changes your job' when cameras check the parts, a move up to engineer, 'a wave of layoffs "
            "at work'",
       needs="[factory worker] first, or [school-leaving certificate]; a short course in measuring and sampling",
       turning="Near the end of the night shift the inspector finds three cracked brackets in a sample of fifty. The "
               "lorry for the buyer leaves at six."),
  dict(name="standards inspector", kind="career", sector="public", sphere="comm", face="comm.W", ways="W U",
       profiles=[("W U", "Checks weights, labels and safety marks the same way for every seller, and writes it all "
                         "down."),
                 ("G", "Knows every trader on the round by name, and keeps the market fair by knowing them.")],
       meets="need:meaning+.05 need:safety+.05 res:money+.05 res:time-.08 res:ties-.03",
       ages=(21, 70), share=.0005,   # estimate (Packs): the council's standards office is a few people in a town;
                                     # most of them came from a shop, a market or an office desk
       say="a standards inspector",
       gained="'a job interview' at the council's standards office after years as [market porter], [office clerk] or "
              "[shop assistant], then a course in weights, labels and food safety",
       lost="the office cut back in a lean budget, a move up to run the office, retirement",
       needs="[market porter], [office clerk] or [shop assistant] first; [school-leaving certificate]; the inspector's "
             "course and warrant card",
       turning="A test purchase shows the corner butcher's scale gives short weight on every bag. He has served the "
               "street for thirty years and carried half of it on credit through hard winters."),
  dict(name="market trader", kind="career", sector="services", sphere="comm", face="comm.R", ways="R B",
       profiles=[("R B", "Sings the prices, haggles on the spot, and takes the van wherever the crowd is."),
                 ("U G", "Knows the margin on every line and the regulars who buy them, week after week.")],
       meets="need:autonomy+.08 need:belonging+.03 need:safety-.05 res:money+.03 res:time-.12 res:health-.03",
       ages=(16, 85), share=.01,   # estimate (Packs): street and market traders are a few workers in 1,000, many for a
                                   # few seasons beside other work
       say="a market trader",
       gained="a pitch of their own after years behind someone else's counter as [shop assistant], [salesperson] or "
              "[market porter]: a permit, a van of stock and the first Saturday",
       lost="a wet summer too many, the pitch fee rising, a shop of their own, a bad back",
       needs="[shop assistant], [salesperson] or [market porter] first; a pitch and a trading permit; stock bought on "
             "[savings] or credit; [selling] helps",
       turning="A new trader sets up across the row with the same stock at half the price. The van is full of stock "
               "bought on credit, and the payment falls due on Monday."),
  dict(name="savings-circle member", kind="community", sphere="comm", face="comm.G", ways="G W",
       profiles=[("G W", "Pays in every month, carries a neighbour through a hard one, and trusts the turn to come."),
                 ("U B R", "Keeps the circle's book to the last coin, and bids for the early pot to stake a venture.")],
       meets="need:belonging+.05 need:safety+.03 res:ties+.03 res:time-.02",
       ages=(16, 95), share=.05,   # estimate (Packs): rotating savings circles are common in many communities, and in
                                   # some neighbourhoods most households belong to one at some time
       say="a member of a savings circle",
       gained="neighbours, workmates or kin who each put the same sum into a pot every month and take it in turn ask "
              "them to join, often after 'your first full-time job'",
       lost="the circle ending its round, a move away, a falling-out over a missed month",
       needs="a steady sum to put in each month, and someone in the circle to vouch for them",
       turning="A member who took the pot early has missed two months, and the member whose turn is last wants her "
               "out."),
  dict(name="detective", kind="career", sector="public", sphere="prot", face="prot.U", ways="U W",
       profiles=[("U W", "Reads the pattern in the reports, follows the evidence, and frees the wrong suspect."),
                 ("B", "Works for the clear-up figures and the next rank, and trades favours for a name.")],
       meets="need:competence+.08 need:meaning+.05 res:money+.05 res:time-.12 res:health-.03",
       ages=(23, 65), share=.002,   # estimate (Packs): about 1 police officer in 5 moves to detective work
       say="a detective",
       gained="years on the beat as [police officer], then the detective's exam and a desk on the station's crime "
              "team; 'a promotion is open'",
       lost="a move back to uniform, 'burnout', retirement, a complaint upheld",
       needs="[police officer] for some years; the detective's course and exam; not [someone with a record]",
       turning="The station wants a quick charge for a run of shed break-ins, and the young man everyone names was "
               "across town on two of the nights."),
  dict(name="private investigator", kind="career", sector="services", sphere="prot", face="prot.B", ways="B U",
       profiles=[("B U", "Takes the cases that pay, names the fee, and brings back facts that hold up."),
                 ("W R G", "Takes on the families no one else listened to, and keeps at it for them.")],
       meets="need:autonomy+.08 need:competence+.05 need:safety-.05 res:money+.03 res:time-.1",
       ages=(21, 75), share=.0005,   # estimate (Packs): US BLS counts about 35,000 private detectives and
                                     # investigators; many work for insurers and lawyers for a few years
       say="a private investigator",
       gained="a small office of their own or a place at an agency, after years as [police officer], [security "
              "guard], [door staff] or [journalist]; the first client from a lawyer or an insurer",
       lost="the work drying up, the licence lapsing, a steady job with an insurer, retirement",
       needs="[police officer], [security guard], [door staff] or [journalist] first in most cases; the investigator's "
             "licence where the law asks for one; not [someone with a record]; [finding things out] helps",
       turning="A father offers a fat fee to find his grown daughter, who moved away three years ago and has not "
               "called since. He will not say why."),
  dict(name="park ranger", kind="career", sector="public", sphere="prot", face="prot.G", ways="G W",
       profiles=[("G W", "Knows every path and every family at the park's edge, and keeps the land for all of them."),
                 ("R", "Goes out alone in any weather, and is first up the hill when someone is lost.")],
       meets="need:meaning+.08 need:autonomy+.05 res:health+.03 res:money+.02 res:time-.1 res:ties-.02",
       ages=(20, 65), share=.0005,   # estimate (Packs): a few thousand ranger posts in a large country, held for
                                     # long stretches
       say="a park ranger",
       gained="'a job interview' with the park's managers after years as [forester], [scout or guide] or "
              "[search-and-rescue volunteer], then a countryside course and a season on trial",
       lost="the post cut in a lean budget, a bad knee, retirement",
       needs="[forester], [scout or guide] or [search-and-rescue volunteer] first, or [knowing the woods]; a countryside "
             "course; [driving licence]",
       turning="In the driest week of the summer a family from the village has a campfire on the heath, where every "
               "fire is banned. The father is someone the ranger has known since school."),
]

