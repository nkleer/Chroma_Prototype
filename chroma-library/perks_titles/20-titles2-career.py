# =============================== TITLES, volume 2 ===============================
# Emren's "Modern Earth: 100 More Titles" (2026-10-05 12:05: "Use this title and perk ideas and implement it to the
# game"), T2-001 to T2-100, written by the Library from Emren's entries (briefs in drafts/titles2/BRIEF.md). Emren's
# profiles and turning points are verbatim; profiles marked "third: Library" are ours, added to keep the colors even.
# Shares are ours (Emren's file makes no prevalence claims). How each is gained and lost: drafts/titles2/roles-v2.py.

# ---------- volume 2, career (T2-001 to T2-045): one at a time, like the careers above
TITLES += [
  # T2-001
  dict(name="laboratory technician", kind="career", sector="knowledge", sphere="care", face="care.U", ways="W U",
       profiles=[("W U", "Keeps results dependable through careful routine."),
                 ("R G", "Learns the living material by daily contact and follows practical curiosity.")],
       meets="need:competence+.08 res:money+.05 res:time-.1 need:autonomy-.03",
       ages=(18, 67), share=.008,   # estimate: the US counts about 330,000 clinical laboratory technologists and
                                    # technicians (BLS), plus research and industry technicians; turnover adds more
       say="a laboratory technician",
       gained="a college course or a science degree, then 'a job interview' and 'your first full-time job' at a bench "
              "in a hospital, school or company laboratory",
       lost="the contract ending, 'a promotion is open' taken, a move into another field; "
            "'new technology changes your job'",
       needs=("[school-leaving certificate]; a technical course or a science degree ([lab work]), and safety training "
              "before laboratory access"),
       turning="At closing time, the technician notices that one culture smells different. Tomorrow's run now depends "
               "on whether they speak up."),
  # T2-002
  dict(name="paramedic", kind="career", sector="public", sphere="care", face="care.R", ways="R W",
       profiles=[("R W", "Acts decisively because somebody needs help now."),
                 ("U", "Finds purpose in practiced assessment and continually improving judgment.")],
       meets="need:meaning+.1 need:belonging+.05 res:money+.05 res:time-.12 res:health-.03",
       ages=(20, 65), share=.004,   # estimate: about 1 UK worker in 1,000 is a paramedic on the HCPC register; more
                                    # have held the post
       say="a paramedic",
       gained=("a paramedic degree with supervised ambulance placements ([emergency care]), registration, then a first "
               "post on a station rota"),
       lost="leaving frontline work, 'a serious accident or illness', 'burnout', retirement",
       needs="[professional registration]; a degree in paramedic science; fitness checks and a [driving licence] for "
             "emergency driving"),
  # T2-003
  dict(name="physician", kind="career", sector="public", sphere="care", face="care.U", ways="W U",
       profiles=[("W U", "Treats sound judgment and accountable care as obligations."),
                 ("B", "Helps people regain control over decisions affecting their lives."),
                 ("G", "Serves one community for decades and comes to know its families across generations.")],
                 # third: Library
       meets="need:meaning+.1 res:money+.12 res:time-.15 res:health-.03",
       ages=(24, 80), share=.008,   # OECD: about 3.7 practising doctors per 1,000 people; retired doctors and those
                                    # who left medicine add more
       say="a doctor",
       gained="five or six years of medical school, supervised years as a junior doctor, then a licence to practise "
              "and a post on a ward or in a practice",
       lost="retirement, a move into another occupation, being struck off after a complaint upheld (the knowledge "
            "stays)",
       needs="[graduate] in medicine; [professional registration]; years of supervised training"),
  # T2-004
  dict(name="psychotherapist", kind="career", sector="knowledge", sphere="care", face="care.U", ways="U G",
       profiles=[("U G", "Learns how a person's history and present circumstances fit together."),
                 ("R", "Makes space for difficult feelings to be expressed honestly."),
                 ("W", "Keeps firm ethical boundaries so clients can rely on the frame of the work.")],   # third: Library
       meets="need:meaning+.1 res:money+.05 res:time-.1 res:health-.02",
       ages=(25, 80), share=.003,   # estimate
       say="a psychotherapist",
       gained=("a long training in [counselling], often after years as a [nurse] or [teacher], with supervised "
               "clients and therapy of their own, then a caseload in a clinic or a private practice"),
       lost="closing the practice, a move into other work, losing [therapy accreditation]",
       needs=("[graduate]; a recognised psychotherapy training and supervision; [therapy accreditation], or "
              "registration where the country requires it")),
  # T2-005
  dict(name="pharmacist", kind="career", sector="services", sphere="care", face="care.U", ways="W U",
       profiles=[("W U", "Keeps an everyday system of medicine use trustworthy."),
                 ("B G", "Builds a durable local practice that supports community continuity and personal "
                         "independence."),
                 ("R", "Enjoys the quick, face-to-face problem-solving of a busy counter.")],   # third: Library
       meets="need:safety+.08 res:money+.1 res:time-.1 res:health-.02",
       ages=(23, 75), share=.002,   # OECD: under 1 practising pharmacist per 1,000 people; estimate for ever
                                    # holding it
       say="a pharmacist",
       gained="a pharmacy degree and a supervised pre-registration year, then a registered post in a high-street or "
              "hospital pharmacy",
       lost="retirement, the pharmacy closing, leaving practice",
       needs="[graduate] in pharmacy; [professional registration]"),
  # T2-006
  dict(name="veterinarian", kind="career", sector="services", sphere="care", face="care.U", ways="U G",
       profiles=[("U G", "Learns the needs of animals within the systems they live in."),
                 ("B R", "Builds an independent practice around a deeply felt commitment to animals.")],
       meets="need:meaning+.1 res:money+.08 res:time-.12 res:health-.03",
       ages=(23, 75), share=.0006,   # US: about 125,000 veterinarians for 330 million people (AVMA); estimate
       say="a vet",
       gained=("five or six years of veterinary school ([handling animals]), then a post in a small-animal clinic or a "
               "farm practice"),
       lost="a move into another role, retirement, closing or selling the practice",
       needs="[graduate] in veterinary medicine; [professional registration]"),
  # T2-007
  dict(name="midwife", kind="career", sector="public", role="women", sphere="care", face="care.G", ways="G W",   # role=women: too few for the CPS; Britain's midwife register has fewer than 1 man in 100, US certified nurse-midwives about 98 in 100 women (NMC; ACNM)
       profiles=[("G W", "Supports a major life transition through continuity and accountable care."),
                 ("U", "Studies and refines a skilled practice while listening to each person's circumstances.")],
       meets="need:meaning+.12 need:belonging+.05 res:money+.05 res:time-.12 res:health-.03",
       ages=(21, 67), share=.001,   # UK: about 45,000 midwives on the NMC register for 67 million people; estimate
       say="a midwife",
       gained="a midwifery degree with supervised births, or a shortened course after years as a [nurse], then a post "
              "on a labour ward or in a community team",
       lost="retirement, a move into other work, losing registration",
       needs="[professional registration]; a midwifery qualification"),
  # T2-008
  dict(name="firefighter", kind="career", sector="public", role="men", sphere="prot", face="prot.R", ways="W R",   # role=men: firefighters 5.1 in 100 women (US BLS CPS 2025, table 11)
       profiles=[("W R", "Joins collective discipline to decisive action."),
                 ("G", "Protects a familiar place and the lives already rooted there.")],
       meets="need:belonging+.1 need:meaning+.08 res:money+.05 res:time-.1 res:health-.05",
       ages=(18, 60), share=.004,   # US: about 360,000 career firefighters and nearly twice as many volunteers (NFPA);
                                    # volunteers are not counted here; estimate
       say="a firefighter",
       gained="an application, fitness and aptitude tests, then weeks at a training centre and a place on a watch",
       lost="retirement, an injury or 'a serious accident or illness', leaving the service",
       needs="age 18 or more; [keeping fit]; not [someone with a record] for most services; a [driving licence] helps"),
  # T2-009
  dict(name="emergency dispatcher", kind="career", sector="public", sphere="prot", face="prot.U", ways="W U",
       profiles=[("W U", "Maintains clear, dependable coordination under pressure."),
                 ("R", "Brings immediate human presence to someone having a terrible day."),
                 ("G", "Feels bound to the district whose calls they take and knows its roads and people by name.")],
                 # third: Library
       meets="need:meaning+.08 res:money+.05 res:time-.12 res:health-.03",
       ages=(18, 67), share=.003,   # US: about 100,000 public safety telecommunicators (BLS), with high turnover;
                                    # estimate
       say="an emergency dispatcher",
       gained="an operator course, then supervised shifts on the phones and the radio in a control room; some come "
              "from the ambulance, the fire service or the police",
       lost="another job, 'burnout', retirement",
       needs="a communications course; background and suitability checks"),
  # T2-010
  dict(name="translator", kind="career", sector="knowledge", ways="U",
       profiles=[("U", "Pursues exact meaning across language and context."),
                 ("W G", "Carries a community's stories into another language without erasing their roots."),
                 ("B", "Builds a freelance business on a rare language pair and sets their own terms.")],
                 # third: Library
       meets="need:autonomy+.08 res:money+.05 res:time-.08 need:safety-.03",
       ages=(20, 80), share=.003,   # estimate: the US counts about 70,000 interpreters and translators (BLS); many
                                    # more translate part-time
       say="a translator",
       gained="a translation degree or years of living in two languages, then a first paid job that turns into "
              "regular clients or a staff post",
       lost="lost clients, 'new technology changes your job' as machine translation spreads, a move into other work, "
            "retirement",
       needs="[second language] at a professional level; a translation qualification, or sworn status for official "
             "papers"),
  # T2-011
  dict(name="journalist", kind="career", sector="knowledge", sphere="gather", face="gather.U", ways="U R",
       profiles=[("U R", "Follows questions and gives discoveries a compelling voice."),
                 ("W", "Reports unglamorous public facts because accountability depends on them."),
                 ("B", "Cultivates sources and exclusives to build a name and influence of their own.")],
                 # third: Library
       meets="need:meaning+.08 res:ties+.05 res:money+.03 res:time-.12 need:safety-.03",
       ages=(18, 75), share=.004,   # estimate
       say="a journalist",
       gained="a journalism course or a student paper, a first commission, then a newsroom job or regular freelance "
              "work",
       lost="'a wave of layoffs at work', a move into another career, leaving the publication",
       needs=("[reporting] and press access, such as a [press card]; [finding things out] helps; a subject specialism "
              "for some beats")),
  # T2-012
  dict(name="book editor", kind="career", sector="knowledge", sphere="arts", face="arts.U", ways="W U",
       profiles=[("W U", "Helps a work become clear, coherent and dependable."),
                 ("B R", "Champions distinctive voices that might otherwise be made harmless."),
                 ("G", "Nurtures writers across many books and keeps a publishing list's character alive.")],
                 # third: Library
       meets="need:competence+.08 res:money+.05 res:time-.1 res:health-.02",
       ages=(21, 75), share=.001,   # estimate
       say="a book editor",
       gained="years as an editorial assistant, then a first manuscript of their own to see through to print",
       lost="the publisher closing or merging, going freelance, another occupation",
       needs="[graduate], usually; [editing] and a real list to work on",
       turning="The cleanest sentence in the manuscript is also the one that sounds least like its author."),
  # T2-013
  dict(name="archivist", kind="career", sector="public", sphere="learn", face="learn.U", ways="G U",
       profiles=[("G U", "Preserves records so future people can understand the past."),
                 ("B", "Protects access to evidence that lets ordinary people challenge powerful accounts."),
                 ("W", "Keeps records complete and in order because institutions answer for their actions through "
                       "them.")],   # third: Library
       meets="need:meaning+.08 need:competence+.05 res:money+.03 res:time-.08",
       ages=(22, 70), share=.0005,   # estimate
       say="an archivist",
       gained="a postgraduate archive course or years of volunteer cataloguing, then a post looking after a collection",
       lost="funding ending, retirement, another post",
       needs=("[graduate]; archival training or proven competence in [archive research]; authorised access to the "
              "records")),
  # T2-014
  dict(name="museum curator", kind="career", sector="public", sphere="learn", face="learn.U", ways="G U",
       profiles=[("G U", "Connects objects, histories and their living contexts."),
                 ("R", "Builds exhibitions that make visitors feel something unexpected."),
                 ("B", "Builds the standing of a collection, and their own, through acquisitions and patrons.")],
                 # third: Library
       meets="need:meaning+.08 need:competence+.03 res:money+.05 res:time-.1 need:autonomy-.03",
       ages=(23, 75), share=.0005,   # estimate
       say="a museum curator",
       gained="a specialist degree and years as an assistant, then a collection that becomes their continuing "
              "responsibility",
       lost="a contract ending, a move to another institution, retirement",
       needs="[graduate], often a postgraduate degree; appointment to the role"),
  # T2-015
  dict(name="archaeologist", kind="career", sector="knowledge", sphere="learn", face="learn.U", ways="U G",
       profiles=[("U G", "Builds careful explanations from material traces."),
                 ("B G", "Works to keep a community's heritage from being defined entirely by outsiders."),
                 ("R", "Is drawn by the excitement of the dig and the moment something emerges from the ground.")],
                 # third: Library
       meets="need:meaning+.08 need:competence+.05 res:money+.03 res:time-.1 need:safety-.03",
       ages=(21, 70), share=.0006,   # estimate
       say="an archaeologist",
       gained="an archaeology degree and a field school, then a place on a commercial dig or a research project",
       lost="project funding ending, a move into another career, retirement",
       needs="[graduate] in archaeology; permission for each project and site"),
  # T2-016
  dict(name="land surveyor", kind="career", sector="knowledge", ways="U W",
       profiles=[("U W", "Makes measurements that others can safely rely on."),
                 ("B", "Builds independent expertise that gives them leverage in their working life.")],
       meets="need:competence+.08 res:money+.08 res:time-.1",
       ages=(18, 70), share=.001,   # US: about 50,000 surveyors (BLS); estimate
       say="a land surveyor",
       gained="a surveying degree or a technician apprenticeship, then responsibility for a survey of their own",
       lost="retirement, a move into other work, losing a licence",
       needs=("[graduate] or the [apprentice] route; a surveying licence or [chartered status] where the country "
              "requires one")),
  # T2-017
  dict(name="urban planner", kind="career", sector="public", ways="W U",
       profiles=[("W U", "Coordinates competing needs into workable long-term arrangements."),
                 ("R G", "Defends the street-level life and places residents actually love."),
                 ("B", "Works the politics of each scheme, trading concessions to get things built.")],
                 # third: Library
       meets="need:meaning+.08 res:money+.05 res:time-.1 need:competence-.02",
       ages=(22, 70), share=.001,   # US: about 40,000 urban and regional planners (BLS); estimate
       say="a town planner",
       gained="a planning degree, then a post on a council or consultancy team assigned to a neighbourhood project",
       lost="another post, restructuring after 'a bitter election', retirement",
       needs="[graduate] in planning or a related field; an actual planning remit"),
  # T2-018
  dict(name="architect", kind="career", sector="knowledge", ways="U R",
       profiles=[("U R", "Turns spatial questions into imaginative structures."),
                 ("G", "Designs additions that belong to a place rather than announcing a signature."),
                 ("W", "Accepts responsibility for buildings that are safe, lawful and usable by everyone.")],
                 # third: Library
       meets="need:competence+.08 res:money+.08 res:time-.12 need:safety-.05",
       ages=(24, 80), share=.002,   # UK: about 40,000 architects on the ARB register; the US about 125,000 (BLS);
                                    # estimate
       say="an architect",
       gained="a long architecture degree and supervised years in practice, the registration exams, then a first "
              "project of their own",
       lost="closing a practice, a move into another career, 'a recession' drying up commissions, retirement",
       needs="[graduate] in architecture; [professional registration]"),
  # T2-019
  dict(name="civil engineer", kind="career", sector="knowledge", role="men", sphere="prod", face="prod.U", ways="W U",   # role=men: civil engineers 21.8 in 100 women (US BLS CPS 2025, table 11)
       profiles=[("W U", "Builds infrastructure whose reliability matters to strangers."),
                 ("B G", "Keeps existing systems useful while negotiating resources and practical control."),
                 ("R", "Enjoys life on site, where problems need solving today and the result is visible.")],
                 # third: Library
       meets="need:competence+.1 res:money+.08 res:time-.1 res:health-.02",
       ages=(21, 75), share=.004,   # US: about 330,000 civil engineers (BLS), about 1 worker in 500; estimate
       say="a civil engineer",
       gained="an engineering degree and a graduate scheme, then a firm or a council entrusting them with a road, "
              "bridge or water project",
       lost="retirement, 'a recession', a move into another field",
       needs="[graduate] in engineering; [chartered status] to sign off major work"),
  # T2-020
  dict(name="data analyst", kind="career", sector="knowledge", sphere="comm", face="comm.U", ways="U",
       profiles=[("U", "Finds patterns and tests whether they mean anything."),
                 ("R W", "Makes evidence understandable so people can challenge an unfair decision."),
                 ("B", "Uses analysis to give their team leverage in budgets and decisions.")],   # third: Library
       meets="need:competence+.08 res:money+.08 res:time-.08 need:autonomy-.02",
       ages=(20, 70), share=.01,   # estimate: a fast-growing title that office, finance and research staff move into
       say="a data analyst",
       gained=("a degree, a course or a spreadsheet that kept growing, then a workplace that asks them to turn records "
               "into answers ([working with data])"),
       lost="'new technology changes your job', 'a wave of layoffs at work', another occupation",
       needs="[graduate] or [writing code]; [finding things out] helps; legitimate access to the records"),
  # T2-021
  dict(name="cybersecurity analyst", kind="career", sector="knowledge", role="men", sphere="prot", face="prot.U", ways="U B",   # role=men: information security analysts 15.9 in 100 women (US BLS CPS 2025, table 11)
       profiles=[("U B", "Anticipates weaknesses to preserve control of information."),
                 ("W G", "Protects a community's dependable digital services and accumulated work."),
                 ("R", "Enjoys the live contest of an incident and the hunt for what got in.")],   # third: Library
       meets="need:competence+.1 res:money+.1 res:time-.1 res:health-.03",
       ages=(20, 67), share=.003,   # estimate: information security analysts are about 1 US worker in 1,000 (BLS)
       say="a cybersecurity analyst",
       gained=("a computing degree or years as a [software developer], [keeping systems secure] and certifications, "
               "then a post on a security team"),
       lost="another post, 'burnout', retirement",
       needs="[writing code]; security certifications; explicit authorisation for every test"),
  # T2-022
  dict(name="machinist", kind="career", sector="industry", role="men", sphere="prod", face="prod.U", ways="U W",   # role=men: machinists about 5 in 100 women (US BLS CPS table 11, recent years)
       profiles=[("U W", "Produces precise parts through practiced control and checking."),
                 ("R", "Finds creative satisfaction in skilled material work and responsive problem-solving."),
                 ("G", "Belongs to a workshop tradition and passes its practice on to apprentices.")],
                 # third: Library
       meets="need:competence+.08 res:money+.05 res:time-.1 res:health-.03",
       ages=(17, 67), share=.006,   # US: about 350,000 machinists and tool and die makers (BLS); estimate for ever
                                    # holding it
       say="a machinist",
       gained="an [apprentice] place in an engineering workshop, or years on a factory floor, then jobs of their own "
              "on the lathes and mills",
       lost="a plant closure or 'a wave of layoffs at work', an injury, retirement",
       needs="machine training ([machining]) and workshop safety; usually [apprentice] first"),
  # T2-023
  dict(name="welder", kind="career", sector="industry", role="men", sphere="prod", face="prod.R", ways="R W",   # role=men: welding, soldering and brazing workers about 5 in 100 women (US BLS CPS table 11, recent years)
       profiles=[("R W", "Joins practical discipline with concentrated physical skill."),
                 ("U", "Enjoys mastering how settings and materials produce different results."),
                 ("B", "Takes certified skills to well-paid contract work wherever the jobs are.")],   # third: Library
       meets="need:competence+.08 res:money+.08 res:time-.1 res:health-.05",
       ages=(17, 67), share=.007,   # US: over 400,000 welders, cutters, solderers and brazers (BLS); estimate
       say="a welder",
       gained=("an apprenticeship or a course in [welding] and coded tests passed, then workshop, site or pipeline "
               "work"),
       lost="a move into another trade, an injury, retirement",
       needs="a [welding certificate] for the job; 'learned a skill' several times"),
  # T2-024
  dict(name="plumber", kind="career", sector="industry", role="men", sphere="prod", face="prod.B", ways="U B",   # role=men: plumbers, pipefitters and steamfitters 3.1 in 100 women (US BLS CPS 2025, table 11)
       profiles=[("U B", "Uses diagnosis and a valued trade to build independence."),
                 ("G W", "Keeps households and familiar buildings functioning over years."),
                 ("R", "Enjoys a day of different jobs and the quick fix that sends them on to the next.")],
                 # third: Library
       meets="need:autonomy+.08 res:money+.08 res:time-.12",
       ages=(18, 75), share=.008,   # US: about 480,000 plumbers, pipefitters and steamfitters (BLS); estimate
       say="a plumber",
       gained="an apprenticeship and the trade exams, then a van and a first regular round of jobs",
       lost="an injury, selling the business, retirement",
       needs="[trade ticket] or [building trade]; [gas safety registration] for boiler work"),
  # T2-025
  dict(name="carpenter", kind="career", sector="industry", role="men", sphere="prod", face="prod.G", ways="U G",   # role=men: carpenters 3.1 in 100 women (US BLS CPS 2025, table 11)
       profiles=[("U G", "Understands material and adapts a design to its properties."),
                 ("B", "Builds a livelihood where skill gives control over clients and working terms.")],
       meets="need:competence+.08 res:money+.05 res:time-.1 need:safety-.03",
       ages=(17, 75), share=.012,   # US: about 940,000 carpenters (BLS), about 1 worker in 170; estimate
       say="a carpenter",
       gained="an apprenticeship or a workshop course, then paid commissions on sites, in joinery shops or for "
              "private clients",
       lost="retirement, an injury, work drying up in 'a recession'",
       needs="[building trade] or [trade ticket]; [tools of one's own]"),
  # T2-026
  dict(name="baker", kind="career", sector="industry", sphere="prod", face="prod.G", ways="G W",
       profiles=[("G W", "Keeps a dependable food tradition alive through daily practice."),
                 ("U R", "Tests unusual combinations and learns from each batch."),
                 ("B", "Runs the bake as a small business of their own and sets its terms.")],   # third: Library
       meets="need:belonging+.05 res:money+.03 res:time-.12 res:health-.03",
       ages=(16, 70), share=.006,   # US: about 200,000 bakers (BLS), with high turnover; estimate
       say="a baker",
       gained="early shifts as a bakery assistant, often after work as a [cook] or a [shop assistant], that become "
              "responsibility for the bake",
       lost="the bakery closing, another job, opening a business of their own after "
            "'a chance to start a business of your own'",
       needs="[baking] and a [food hygiene certificate]"),
  # T2-027
  dict(name="cleaner", kind="career", sector="services", ways="W",
       profiles=[("W", "Makes shared spaces usable through work others often overlook."),
                 ("B", "Uses an accessible route to income and negotiates a more independent working life."),
                 ("G", "Looks after the same homes and buildings for years and knows the people in them.")],
                 # third: Library
       meets="res:money+.03 need:safety+.02 res:time-.1 res:health-.03 need:autonomy-.03",
       ages=(16, 80), share=.08,   # estimate: janitors, cleaners and housekeepers are about 2 US workers in 100 (BLS),
                                   # with high turnover
       say="a cleaner",
       gained="an agency placement, 'a job interview' at a contract firm, or a first household client that becomes "
              "regular work",
       lost="changing clients, an injury, another job",
       needs="a short induction and the right equipment",
       turning="The building is empty except for the cleaner and one exhausted worker. Each knows a side of the "
               "workplace the managers rarely see."),
  # T2-028
  dict(name="sanitation worker", kind="career", sector="public", role="men", ways="W G",   # role=men: refuse and recyclable material collectors about 8 in 100 women (US BLS CPS table 11, recent years)
       profiles=[("W G", "Maintains an essential shared cycle that lets a neighbourhood function."),
                 ("R", "Values active work, direct practical results and crew camaraderie."),
                 ("B", "Values a secure, unionised wage that pays for the life they want outside work.")],
                 # third: Library
       meets="need:belonging+.05 res:money+.05 res:time-.1 res:health-.05",
       ages=(18, 65), share=.003,   # estimate: refuse and recycling collectors are about 1 US worker in 1,000 (BLS)
       say="a refuse collector",
       gained="a council or a contractor taking them onto a collection crew",
       lost="outsourcing, an injury or 'a serious accident or illness', retirement",
       needs="age 18 or more; operational training; a [lorry or bus licence] to drive the truck"),
  # T2-029
  dict(name="postal worker", kind="career", sector="public", ways="G W",
       profiles=[("G W", "Becomes part of the dependable rhythm of a neighbourhood."),
                 ("B", "Values a route and competence that provide a degree of practical independence.")],
       meets="need:belonging+.05 res:money+.05 res:time-.1 res:health-.03",
       ages=(17, 67), share=.01,   # US Postal Service: about 640,000 employees, about 1 worker in 250; estimate
       say="a postal worker",
       gained="a delivery round that becomes their regular assignment",
       lost="restructuring as letters dwindle ('new technology changes your job'), an injury, retirement",
       needs="the employer induction; a [driving licence] for van rounds",
       turning="The person who always waits at the gate has not appeared for several days. Familiarity becomes a "
               "small responsibility."),
  # T2-030
  dict(name="train driver", kind="career", sector="services", role="men", ways="W U",   # role=men: locomotive engineers and operators a few in 100 women (US BLS CPS table 11, recent years); Britain about 1 train driver in 10 a woman (ASLEF)
       profiles=[("W U", "Practises reliable control within a coordinated public system."),
                 ("R", "Loves the embodied concentration and movement of the work.")],
       meets="need:competence+.08 res:money+.08 res:time-.12 res:health-.02",
       ages=(20, 65), share=.001,   # estimate: Britain has about 20,000 train drivers (ASLEF), about 1 worker in 1,600
       say="a train driver",
       gained="a selection process, a year or more of training and assessment, then a driving roster of their own",
       lost="retirement, another role, failing a medical or losing the [train driving licence]",
       needs=("age 20 or more; a [train driving licence] and regular medicals; not [someone with a record] for most "
              "operators")),
  # T2-031
  dict(name="commercial pilot", kind="career", sector="services", role="men", ways="U W",   # role=men: aircraft pilots and flight engineers about 7 in 100 women (US BLS CPS table 11, recent years); about 5 in 100 airline pilots worldwide (ISWAP)
       profiles=[("U W", "Works through disciplined technical mastery and shared procedures."),
                 ("G", "Finds belonging in a multigenerational flying community and its practical traditions."),
                 ("R", "Loves flight itself: the takeoff, the weather and the view from the flight deck.")],
                 # third: Library
       meets="need:competence+.08 res:money+.1 res:time-.12 res:ties-.05",
       ages=(19, 65), share=.001,   # US: about 140,000 airline and commercial pilots (BLS); estimate
       say="an airline pilot",
       gained=("years of flight training ([navigation]) paid with loans or [savings], or a military flying career, "
               "then a type rating and a first commercial post"),
       lost="retirement at 65, 'a wave of layoffs at work' or 'a pandemic and a lockdown', losing the medical "
            "certificate",
       needs="a commercial or [airline pilot licence] and a first-class medical; not [someone with a record]"),
  # T2-032
  dict(name="merchant seafarer", kind="career", sector="services", role="men", sphere="prod", face="prod.R", ways="R G",   # role=men: women are about 1.3 in 100 of the world's seafarers (BIMCO and ICS Seafarer Workforce Report 2021; ILO)
       profiles=[("R G", "Finds a life in movement, physical work and a shipboard community."),
                 ("W B", "Uses demanding service and clear responsibilities to build an independent livelihood.")],
       meets="need:belonging+.05 res:money+.08 res:ties-.1 res:time-.1 res:freedom-.05",
       ages=(16, 65), share=.001,   # estimate: rich countries now supply a small share of the world's 1.9 million
                                    # seafarers (BIMCO and ICS)
       say="a seafarer",
       gained="a cadetship or a maritime course, then a first contracted voyage and [sea legs]",
       lost="a shore job, often after 'a child is born'; an injury, retirement",
       needs="[seafarer's papers]: maritime safety training, a seafarer medical and identity papers",
       turning="A message from home arrives during a watch. They can reply, but they cannot be there."),
  # T2-033
  dict(name="commercial fisher", kind="career", sector="farm", role="men", sphere="prod", face="prod.G", ways="G B",   # role=men: US fishing and hunting workers too few in the CPS to show; women about 1 in 7 of the world's primary fisheries and fish-farming workforce and far fewer on boats at sea (FAO SOFIA 2022; ILO Work in Fishing)
       profiles=[("G B", "Builds a livelihood through a place's waters, seasons and difficult resource choices."),
                 ("U", "Studies patterns and revises practice rather than relying only on inherited habits.")],
       meets="need:autonomy+.08 res:money+.05 need:safety-.05 res:time-.12 res:health-.03",
       ages=(16, 75), share=.001,   # estimate: the EU fishing fleet employs about 130,000 people for 450 million (EU
                                    # STECF)
       say="a fisher",
       gained="a place on a boat, often a [family business], that becomes a continuing livelihood",
       lost="quotas or a closed fishery, selling the boat, an injury, retirement",
       needs="sea safety training ([sea survival certificate]), a berth on a vessel and a [fishing licence]"),
  # T2-034
  dict(name="forester", kind="career", sector="farm", sphere="prod", face="prod.G", ways="G U",
       profiles=[("G U", "Understands growth and manages decisions across long time horizons."),
                 ("W B", "Negotiates obligations and resources to keep land management viable and accountable.")],
       meets="need:meaning+.08 res:money+.05 res:time-.1 need:autonomy-.02",
       ages=(18, 70), share=.0005,   # estimate
       say="a forester",
       gained=("a forestry degree or apprenticeship ([knowing the woods]), then a land manager, an estate or a state "
               "forest taking them on"),
       lost="retirement, a change of management, a move into another field",
       needs="[graduate] or the [apprentice] route; real authority over the woodland"),
  # T2-035
  dict(name="professional beekeeper", kind="career", sector="farm", sphere="prod", face="prod.G", ways="G U",
       profiles=[("G U", "Learns colony behaviour and seasonal relationships through observation."),
                 ("B R", "Turns a consuming fascination into a business of their own."),
                 ("W", "Keeps careful records and follows the health rules that protect neighbouring apiaries.")],
                 # third: Library
       meets="need:autonomy+.08 need:meaning+.08 need:safety-.05 res:money+.02 res:time-.08",
       ages=(20, 85), share=.0003,   # estimate: of about 600,000 beekeepers in the EU, a small minority keep enough
                                     # hives to live from them
       say="a beekeeper",
       gained="'a new hobby you cannot put down' that grows from a few hives to hundreds, with honey, pollination and "
              "queens sold as a business; some farmers add it",
       lost="heavy colony losses, selling the operation, going back to a few hives",
       needs="years of [beekeeping]; land where [hives of one's own] may stand; hive registration and health rules",
       turning="The calendar says one thing; the colonies suggest another. Experience and plans must meet."),
  # T2-036
  dict(name="funeral director", kind="career", sector="services", sphere="faith", face="faith.G", ways="W G",
       profiles=[("W G", "Supports continuity and shared rituals after a death."),
                 ("U R", "Helps families create an unfamiliar but meaningful form of farewell."),
                 ("B", "Keeps a family firm independent and viable beside the large chains.")],   # third: Library
       meets="need:meaning+.08 res:money+.05 res:time-.12 res:health-.02",
       ages=(20, 75), share=.0005,   # estimate
       say="a funeral director",
       gained="a trainee post in a funeral home, often a [family business], then arranging funerals of their own",
       lost="retirement, closing or selling the business, another occupation",
       needs="funeral service training; tact, a [strong stomach] and practical competence",
       turning="The family cannot agree on a single religious tradition, but everyone remembers the same song."),
  # T2-037
  dict(name="civil celebrant", kind="career", sector="services", sphere="arts", face="arts.W", ways="R W",
       profiles=[("R W", "Gives public form to personally meaningful promises and farewells."),
                 ("U", "Carefully designs language and structure to fit each occasion."),
                 ("G", "Marks the weddings, namings and funerals of one town's families across the years.")],
                 # third: Library
       meets="need:meaning+.08 res:ties+.05 res:money+.02 res:time-.05 need:safety-.02",
       ages=(25, 85), share=.0005,   # estimate: Australia has several thousand authorised marriage celebrants for 26
                                     # million people, most of them part-time
       say="a celebrant",
       gained=("a celebrant course and [celebrant authorisation], then a first ceremony that leads to bookings; often "
               "after leading 'a memorial service for a friend' or a wedding in the family"),
       lost="retirement, losing [celebrant authorisation], ending the practice",
       needs=("[public speaking]; celebrant training in [leading a ceremony], and [celebrant authorisation] for "
              "marriages")),
  # T2-038
  dict(name="tattoo artist", kind="career", sector="services", sphere="arts", face="arts.B", ways="R B",
       profiles=[("R B", "Builds a distinctive practice around expression and bodily self-authorship."),
                 ("W U", "Finds creative purpose in precise craft, careful preparation and accountable client care."),
                 ("G", "Keeps a craft lineage alive and serves the same regulars over many years.")],
                 # third: Library
       meets="need:autonomy+.08 res:money+.05 res:time-.1 res:health-.02",
       ages=(18, 75), share=.001,   # estimate
       say="a tattoo artist",
       gained="a portfolio and an apprenticeship in a studio, then a chair and clients of their own",
       lost="the studio closing, an injury to the hand, another occupation",
       needs="[drawing and painting]; hygiene training and a [tattoo licence] for the studio; age 18 or more",
       turning="A client brings a sketch that is awkwardly drawn and deeply important. The artist must improve the "
               "design without replacing its meaning."),
  # T2-039
  dict(name="sound engineer", kind="career", sector="knowledge", sphere="arts", face="arts.U", ways="U R",
       profiles=[("U R", "Solves technical problems in pursuit of an expressive result."),
                 ("W G", "Keeps a venue or musical tradition sounding dependable across generations of performers."),
                 ("B", "Builds a studio and a client list that let them choose their own projects.")],
                 # third: Library
       meets="need:competence+.08 res:ties+.05 res:money+.03 need:safety-.03 res:time-.1",
       ages=(18, 70), share=.002,   # estimate
       say="a sound engineer",
       gained="small paid sessions in a studio or at a venue that turn into regular bookings",
       lost="hearing loss or other health limits, lost work, a move into another field",
       needs="[sound mixing] and access to equipment; a [musical instrument] often comes first"),
  # T2-040
  dict(name="stage technician", kind="career", sector="services", ways="W U",
       profiles=[("W U", "Makes an apparently effortless performance possible through preparation."),
                 ("B R", "Enjoys turning audacious ideas into workable effects while building a valued niche."),
                 ("G", "Belongs to a crew that travels together and looks after its own.")],   # third: Library
       meets="need:belonging+.08 res:money+.05 res:time-.12 res:health-.03",
       ages=(17, 65), share=.003,   # estimate
       say="a stage technician",
       gained="a venue or a touring crew taking them on, often after helping with school or amateur shows",
       lost="a tour ending, an injury, venues closing in 'a pandemic and a lockdown', a move into another occupation",
       needs="[stagecraft]; a [rigging ticket] and electrical tickets for restricted equipment"),
  # T2-041
  dict(name="video-game developer", kind="career", sector="knowledge", ways="U R",
       profiles=[("U R", "Creates systems that let other people explore interesting possibilities."),
                 ("W G", "Builds games that preserve cultural practices and support shared play."),
                 ("B", "Founds an independent studio to own their work and what it earns.")],   # third: Library
       meets="need:meaning+.05 res:money+.08 res:time-.12 need:safety-.03",
       ages=(18, 67), share=.002,   # estimate
       say="a game developer",
       gained="a studio job, or an independent game that earns enough to keep going",
       lost="the studio closing or 'a wave of layoffs at work', 'burnout', a change of field",
       needs="[writing code] or [drawing and painting]; a real job or a viable project"),
  # T2-042
  dict(name="professional athlete", kind="career", sector="services", ways="R W",
       profiles=[("R W", "Lives a demanding practice through discipline, competition and immediate performance."),
                 ("U", "Approaches performance through careful learning and deliberate refinement.")],
       meets="need:belonging+.08 res:money+.05 res:time-.12 res:freedom-.03 res:health-.03 need:safety-.03",
       ages=(16, 40), share=.001,   # estimate: paid professionals are a small fraction of those who play organised
                                    # sport
       say="a professional athlete",
       gained="years of 'tryouts for the team' and youth academies, then a club contract or prize money enough to "
              "live on",
       lost="an injury or 'a serious accident or illness', losing selection, retiring from competition in their "
            "thirties",
       needs="[on the team] for years; ability and [keeping fit], eligibility for the sport and a paid contract"),
  # T2-043
  dict(name="novelist", kind="career", sector="knowledge", sphere="arts", face="arts.R", ways="R",
       profiles=[("R", "Gives felt experience an invented form other people can inhabit."),
                 ("U", "Builds stories through structure, constraints and patient revision."),
                 ("W", "Organises the work around an obligation to tell a neglected community's story faithfully.")],
                 # third: Library, from Emren's own example ("the White novelist")
       meets="need:meaning+.08 need:autonomy+.08 need:safety-.05 res:money+.02 res:time-.08",
       ages=(20, 95), share=.0005,   # estimate: far fewer people live as novelists than ever publish a novel
       say="a novelist",
       gained="years of writing alone, then a first published book or commission and a second; "
              "'the notebooks come together'",
       lost="choosing another occupation or stopping professional writing; the books remain",
       needs="a long writing practice ([writing stories]); publication ([book in print]) or commissioned work",
       turning="A publisher likes the book but asks for an ending the novelist no longer believes."),
  # T2-044
  dict(name="court interpreter", kind="career", sector="public", ways="W U",
       profiles=[("W U", "Protects accurate understanding in a consequential formal process."),
                 ("B G", "Ensures people retain their own voice when crossing an unfamiliar institution.")],
       meets="need:meaning+.08 res:money+.05 res:time-.1 res:health-.02",
       ages=(23, 75), share=.0003,   # estimate
       say="a court interpreter",
       gained=("an interpreting qualification and [court interpreter accreditation], then continuing assignments; "
               "often after years as a [translator]"),
       lost="losing [court interpreter accreditation], a move into another field, retirement",
       needs=("[second language]; an interpreting qualification ([interpreting]); court approval and a background "
              "check ([court interpreter accreditation])"),
       turning="A short answer contains an ambiguity that could matter greatly. The room is impatient for the next "
               "question."),
  # T2-045
  dict(name="professional conservator", kind="career", sector="knowledge", ways="G U",
       profiles=[("G U", "Learns how materials age and preserves what can responsibly survive."),
                 ("R", "Is moved by the singular presence of an object and wants others to encounter it."),
                 ("W", "Follows professional ethics so that every treatment is documented and, where possible, "
                       "reversible.")],   # third: Library
       meets="need:meaning+.08 need:competence+.08 res:money+.03 res:time-.1 need:autonomy-.02",
       ages=(23, 75), share=.0002,   # estimate
       say="a conservator",
       gained=("a conservation degree and supervised internships in [restoring old things], then objects entrusted to "
               "their care"),
       lost="funding ending, another occupation, retirement",
       needs="[graduate] in conservation; permission from the institution or owner holding the objects",
       turning="The damage is part of the object's history. Removing every mark would also remove part of its "
               "story."),
]

