# =============================== PERKS, volume 2 ===============================
# Asked for by Emren (2026-10-05 15:46: "can you generate more related, realistic perks?"; 15:47: RimWorld as
# inspiration). The licences, trainings, tools and standing that the 100 titles of volume 2 need, and everyday perks
# that make ordinary lives richer. RimWorld's skills served as a checklist; its traits stay the engine's temperament,
# except learned, concrete capacities (a strong stomach, sea legs). Notes: drafts/perks2/*-notes.md.

# ---------- volume 2, skill: what the hands, the body or the head can do; it fades by skill_half once unused
PERKS += [
  # trades and making
  dict(name="welding", kind="skill", ways="R U", odds=.03, skill_half=10, retires=None,
       ages=(16, 85), share=.03,   # estimate: the US counts about 420,000 welders, cutters and brazers at work (BLS);
                                   # farmers, mechanics and hobbyists who can weld add more
       say="can weld",
       gained="a welding course or an [apprentice] place and coded tests passed as a [welder]; a farmyard or a garage "
              "where things keep breaking",
       lost="years without striking an arc; the eyes and the lungs",
       needs="'learned a skill' several times; a mask, a set and a safe place to work"),
  dict(name="machining", kind="skill", ways="U W", odds=.03, skill_half=10, retires=None,
       ages=(16, 85), share=.015,   # estimate: the US counts about 370,000 machinists and tool makers at work (BLS);
                                    # school and college workshops and model engineers add some
       say="can work a lathe and a mill",
       gained="an engineering [apprentice] place, years on a factory floor, a model engineer's shed; holding it as a "
              "[machinist]",
       lost="years away from the machines; computer-run machines change the work ('new technology changes your job')",
       needs="'learned a skill' several times; workshop safety first"),
  dict(name="baking", kind="skill", ways="G W", odds=.03, skill_half=20, retires=None,
       ages=(8, 100), share=.12,   # estimate: bread and pastry from scratch, beyond a cake from a packet
       say="can bake",
       gained="a grandparent's kitchen, 'learning to cook for yourself', a sourdough starter kept alive through "
              "'a pandemic and a lockdown'; early shifts as a [baker]",
       lost="only the hands and the years; a flat with no oven suspends it",
       needs="'learned a skill'"),
  dict(name="restoring old things", kind="skill", ways="G U", odds=.03, skill_half=20, retires=None,
       ages=(14, 100), share=.03,   # estimate: furniture, clocks, old cars, books and frames
       say="can bring old things back to life",
       gained="a chair rescued from a skip, an old car in the garage, 'a broken lamp at the repair cafe'; training as a "
              "[professional conservator]",
       lost="only the eyes and the hands",
       needs="[fixing things] or [sewing and mending]; patience"),
  # sea, land and living things
  dict(name="navigation", kind="skill", ways="U R", odds=.04, skill_half=15, retires=None,
       ages=(10, 95), share=.06,   # estimate: map and compass, charts, the instruments of a cockpit
       say="can navigate",
       gained="a [scout or guide] troop, 'a weekend hike' that went wrong, flight training as a [commercial pilot], "
              "the training of a [search-and-rescue volunteer]",
       lost="years of letting the phone do it",
       needs="'learned a skill'"),
  dict(name="boat handling", kind="skill", ways="R G W", odds=.03, skill_half=15, retires=None,
       ages=(8, 90), share=.05,   # estimate: the US boating industry counts about 85 million Americans out on the water
                                  # in a year (NMMA), most of them as passengers
       say="can handle a boat",
       gained="a sailing club at 'summer camp', an uncle's dinghy, a berth as a [commercial fisher] or a "
              "[merchant seafarer], the training of a [lifeboat volunteer]",
       lost="years ashore; the knees",
       needs="[swimming]"),
  dict(name="sea legs", kind="skill", ways="R", odds=.02, skill_half=1, retires=None,
       ages=(14, 85), share=.03,   # estimate: seafarers, fishers, ferry crews and sailors who go out in all weathers
       say="has sea legs",
       gained="the first rough weeks of a voyage as a [merchant seafarer] or a [commercial fisher], or winters of "
              "[boat handling]",
       lost="a year or two ashore; a few days at sea bring them back",
       needs="[boat handling], or a berth"),
  dict(name="knowing the woods", kind="skill", ways="G", odds=.03, skill_half=25, retires=None,
       ages=(6, 100), share=.06,   # estimate: the names of trees, what can be picked and eaten, tracks and weather
       say="knows the woods",
       gained="a grandparent's walks, [hunting and fishing], a [scout or guide] troop, 'a long walk alone'; years as a "
              "[forester]",
       lost="a move to the city and years away",
       needs="woods within reach"),
  dict(name="handling animals", kind="skill", ways="G W", odds=.04, skill_half=20, retires=None,
       ages=(6, 100), share=.1,   # estimate: farms, stables, kennels, shelters and surgeries
       say="is good with animals",
       gained="a farm childhood, 'a pet of your own', weekends at the shelter as an [animal-shelter campaigner], "
              "training as a [veterinarian]",
       lost="years without animals around",
       needs="'helped someone in need', or an animal in the house"),
  dict(name="beekeeping", kind="skill", ways="G", odds=.02, skill_half=15, retires=None,
       ages=(12, 95), share=.006,   # UK: about 45,000 beekeepers have hives registered on the National Bee Unit's
                                    # BeeBase, about 1 person in 1,500; many give up within a few years
       say="can keep bees",
       gained="a local association's course and a first swarm in [hives of one's own]; 'a new hobby you cannot put "
              "down'; years as a [professional beekeeper]",
       lost="'a third of the hives dead after winter' and no heart to start again; years without hives",
       needs="a place for a hive; 'learned a skill'"),
  # words and records
  dict(name="interpreting", kind="skill", ways="U G", odds=.04, skill_half=8, retires=None,
       ages=(16, 95), share=.01,   # estimate: professional and community interpreters, and bilingual staff who are
                                   # asked to interpret
       say="can interpret between languages",
       gained="years of speaking for relatives at the doctor's, an interpreting course, years as a [translator] or a "
              "[court interpreter]",
       lost="years without both languages in use",
       needs="[second language] at a high level"),
  dict(name="editing", kind="skill", ways="U W", odds=.03, skill_half=15, retires=None,
       ages=(16, 100), share=.02,   # estimate: editors, sub-editors, copy-editors, and academics who edit
       say="can edit a manuscript",
       gained="a student paper, subbing as a [journalist], years as an editorial assistant before becoming a "
              "[book editor]",
       lost="years away from other people's pages",
       needs="[graduate] usually; 'learned a skill' several times"),
  dict(name="reporting", kind="skill", ways="U B", odds=.04, skill_half=8, retires=None,
       ages=(14, 95), share=.008,   # estimate: the US counts about 45,000 news reporters at work (BLS); student and
                                    # local papers add more
       say="can get a story",
       gained="a student paper, a weekly show as a [community-radio presenter], 'a story nobody in town has covered'; "
              "years as a [journalist]",
       lost="years away from the newsroom, contacts gone cold",
       needs="[finding things out]; the nerve to knock on doors"),
  dict(name="writing stories", kind="skill", ways="R", odds=.04, skill_half=15, retires=None,
       ages=(8, 110), share=.03,   # estimate: NaNoWriMo drew about 400,000 writers a year at its height; finishing a
                                   # book is rarer
       say="writes stories",
       gained="years of notebooks, 'inspiration strikes', 'the notebooks come together'; a long practice before "
              "becoming a [novelist]",
       lost="years of not writing",
       needs="'learned a skill' several times"),
  dict(name="archive research", kind="skill", ways="U G", odds=.03, skill_half=15, retires=None,
       ages=(16, 105), share=.02,   # estimate: historians, archivists, and family historians in the record office
       say="knows their way round an archive",
       gained="a family tree begun after 'a grandparent dies', a history degree, training as an [archivist], a "
              "[doctoral graduate]'s years in the reading room",
       lost="years away from the reading room",
       needs="[finding things out]"),
  # science and systems
  dict(name="lab work", kind="skill", ways="U W", odds=.04, skill_half=8, retires=None,
       ages=(16, 85), share=.03,   # estimate: laboratory technicians and scientists, and science graduates with years
                                   # at the bench
       say="is at home at a lab bench",
       gained="a science degree, safety training and a bench as a [laboratory technician], 'the same two hundred "
              "samples a day'",
       lost="years away from the bench; methods moving on",
       needs="[school-leaving certificate]; a technical course or a degree"),
  dict(name="working with data", kind="skill", ways="U B", odds=.05, skill_half=5, retires=None,
       ages=(14, 95), share=.08,   # estimate: statistics, spreadsheets and databases, beyond adding up a column
       say="can make sense of data",
       gained="a statistics course, a spreadsheet that kept growing, 'new technology changes your job'; a post as a "
              "[data analyst]",
       lost="the tools moving on every five years",
       needs="'learned a skill' several times; [bookkeeping] or [writing code] helps"),
  dict(name="keeping systems secure", kind="skill", ways="U B", odds=.03, skill_half=3, retires=None,
       ages=(14, 85), share=.008,   # estimate: ISC2 counts about 5.5 million people in security work worldwide
                                    # (Cybersecurity Workforce Study, 2023), a few workers in 1,000 in rich countries
       say="knows how to keep systems secure",
       gained="years as a [software developer], certifications, a post as a [cybersecurity analyst]; a breach caught "
              "in time",
       lost="a few years out: the threats change every season",
       needs="[writing code]; authorisation for every test"),
  # stage and sound
  dict(name="sound mixing", kind="skill", ways="U R", odds=.03, skill_half=8, retires=None,
       ages=(12, 90), share=.02,   # estimate: engineers, and the volunteers at the desk in halls, churches and pubs
       say="can mix sound",
       gained="running the desk for a band, a church or a pub gig; a weekly show as a [community-radio presenter]; "
              "regular bookings as a [sound engineer]",
       lost="hearing loss; years away from the desk",
       needs="'learned a skill'; a [musical instrument] often comes first"),
  dict(name="stagecraft", kind="skill", ways="W R", odds=.03, skill_half=10, retires=None,
       ages=(12, 85), share=.02,   # estimate: lights, scenery, rigging and the running of a show
       say="knows how to run a stage",
       gained="'the school play' from the wings, amateur shows, a touring crew as a [stage technician]",
       lost="years away from the theatre",
       needs="[fixing things] helps; a [head for heights] for the rig"),
  dict(name="singing", kind="skill", ways="R G W", odds=.03, skill_half=10, retires=None,
       ages=(5, 100), share=.15,   # Chorus America (2019) counts about 54 million Americans who sing in choruses;
                                   # fewer in Europe; estimate for a trained voice
       say="can sing",
       gained="a school choir, hymns as a [regular worshipper], 'an open rehearsal at the community choir', years as "
              "a [choir member]",
       lost="years of silence; the voice in great age",
       needs="'learned a skill'"),
  # people
  dict(name="counselling", kind="skill", ways="G U", odds=.04, skill_half=15, retires=None,
       ages=(18, 100), share=.02,   # estimate: counsellors, therapists, chaplains and helpline volunteers
       say="can counsel people",
       gained="a helpline's training after 'helped someone in need' many times; pastoral work as an "
              "[ordained religious minister]; the long training of a [psychotherapist]",
       lost="years away from the work",
       needs="[calming people down]; supervision"),
  dict(name="leading a ceremony", kind="skill", ways="W G", odds=.03, skill_half=15, retires=None,
       ages=(16, 100), share=.01,   # estimate: clergy, celebrants, funeral directors and lay leaders
       say="can lead a ceremony",
       gained="'a memorial service for a friend' that someone had to lead; celebrant training as a [civil celebrant]; "
              "years as an [ordained religious minister] or a [lay religious teacher]",
       lost="years of not standing up in front",
       needs="[public speaking]"),
  dict(name="settling disputes", kind="skill", ways="W U", odds=.04, skill_half=12, retires=None,
       ages=(18, 100), share=.02,   # estimate: mediators, union reps, managers and elders who are asked
       say="can settle a dispute",
       gained="mediation training as a [community-mediation volunteer], years as a [union rep] or a [shift manager], "
              "a quarrel over a fence settled without a feud",
       lost="a side taken in public; years away from it",
       needs="[calming people down]; a name for fairness"),
  dict(name="organising people", kind="skill", ways="W B", odds=.05, skill_half=10, retires=None,
       ages=(12, 100), share=.2,   # estimate: anyone who has run a club, a fair or a team of volunteers; about 1 adult in 5 (was .15)
       say="gets people organised",
       gained="the year's events as a [parent-association organiser], a street party that grew into a "
              "[festival organiser]'s job, 'the club or congregation asks you to lead'",
       lost="years of letting others do it",
       needs="'made a friend' several times"),
  dict(name="campaigning", kind="skill", ways="R B", odds=.04, skill_half=8, retires=None,
       ages=(14, 100), share=.03,   # estimate
       say="can run a campaign",
       gained="'a sense of injustice' and a petition, 'a protest to save the local hospital', years as a "
              "[civil-liberties campaigner] or a [disability-rights organiser]",
       lost="'burnout'; years out of it",
       needs="'defied an authority' or 'helped someone in need'"),
  dict(name="handling red tape", kind="skill", ways="B", odds=.04, skill_half=5, retires=None,
       ages=(16, 110), share=.1,   # estimate: carers, migrants, the self-employed and the parents of children with
                                   # support needs learn it the hard way
       say="knows their way through red tape",
       gained="years as a [parent coordinating complex support needs] or a [carer for a parent]; a claim as an "
              "[asylum applicant]; 'your first tax form and a stack of bills'",
       lost="the rules changing every few years",
       needs="patience; 'learned a skill'"),
  # the body: capacities that practice builds and disuse takes away
  dict(name="emergency care", kind="skill", ways="W R", odds=.04, skill_half=3, retires=None,
       ages=(16, 85), share=.02,   # estimate: paramedics, emergency staff, firefighters and rescue volunteers, beyond a
                                   # first-aid course
       say="knows emergency care",
       gained="a degree and ambulance placements as a [paramedic], training as a [firefighter] or a "
              "[search-and-rescue volunteer]; 'a stranger saves you, or you save one'",
       lost="years off the road: the know-how fades fast",
       needs="[first-aid certificate] first"),
  dict(name="strong stomach", kind="skill", ways="B", odds=.02, skill_half=5, retires=None,
       ages=(16, 110), share=.05,   # estimate
       say="has a strong stomach",
       gained="years on the ambulance as a [paramedic], in a funeral home as a [funeral director], on a farm or a "
              "ward; 'a serious accident or illness' faced up close",
       lost="years away from it",
       needs="the first bad day got through"),
  dict(name="used to night shifts", kind="skill", ways="W B", odds=.02, skill_half=1, retires=None,
       ages=(16, 75), share=.15,   # about 1 worker in 5 in the EU works at night at least once a month (Eurofound,
                                   # European Working Conditions Survey 2015); estimate for those whose body adjusts
       say="is used to night shifts",
       gained="a year of nights as a [nurse], a [paramedic] or an [emergency dispatcher], early starts as a [baker], "
              "a night line in a factory",
       lost="a day job and a year of normal sleep; the nights grow harder after sixty",
       needs="a job that runs through the night"),
  dict(name="head for heights", kind="skill", ways="R B", odds=.02, skill_half=3, retires=None,
       ages=(12, 90), share=.06,   # estimate: scaffolders, roofers, riggers, firefighters and climbers
       say="has a head for heights",
       gained="a climbing wall, scaffolding as a [builder], the rig as a [stage technician], ladders as a [firefighter]",
       lost="a fall, or years on the ground",
       needs="'took a wild risk' the first time"),
  dict(name="keeping fit", kind="skill", ways="R B", odds=.04, skill_half=2, retires=None,
       ages=(8, 100), share=.3,   # about 6 adults in 10 in England are active 150 minutes a week (Sport England,
                                  # Active Lives); estimate for those who train on purpose for years
       say="keeps fit",
       gained="'a band or a sport that takes over your life', years [on the team], 'a warning from the doctor' taken "
              "seriously; the fitness tests of a [firefighter]",
       lost="a year or two of stopping; an injury",
       needs="time and a pair of shoes"),
]

