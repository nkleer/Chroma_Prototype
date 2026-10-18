# =============================== TITLES ===============================

# ---------- career: one at a time; the shares add up to about two of these kinds of work per life
TITLES += [
  dict(name="shop assistant", kind="career", sector="services", sphere="comm", face="comm.R", ways="G R",
       meets="need:belonging+.05 res:money+.05 res:time-.1 need:autonomy-.05",
       ages=(14, 80), share=.45,   # estimate: retail is the commonest first job in rich countries
       say="a shop assistant",
       gained="'a Saturday job at the corner shop', 'your first real job', or 'a new job at last' behind a till",
       lost="better pay elsewhere, the shop closing, 'losing your job'",
       needs="age 14 or more for Saturday work"),
  dict(name="waiter or bartender", kind="career", sector="services", sphere="gather", face="gather.R", ways="R B",
       meets="need:belonging+.05 res:money+.05 res:time-.1 res:health-.03",
       ages=(16, 65), share=.3,   # estimate: hospitality is the other great first job
       say="a waiter",
       gained="'your first real job' in a busy café, a friend who knows the manager, tips from the first night",
       lost="a better job, the place closing, a manager's bad week; 'running on empty' after too many late shifts",
       needs="age 16 or more; 18 to serve drink in most places"),
  dict(name="care worker", kind="career", sector="public", role="women", sphere="care", face="care.W", ways="G W",   # role=women: nursing assistants 86.9, home health aides 86.1, personal care aides 79.8 in 100 women (US BLS CPS 2025, table 11)
       meets="need:meaning+.1 need:belonging+.05 res:money+.02 res:time-.1 res:health-.05",
       ages=(17, 75), share=.08,   # estimate: social care employs about 1 worker in 20 in the UK, with high turnover
       say="a care worker",
       gained="a short course and 'a new job at last' in a care home or on a round of home visits",
       lost="'burnout', low pay, a better offer",
       needs="a background check"),
  dict(name="office clerk", kind="career", sector="services", role="women", sphere="comm", face="comm.U", ways="W U",   # role=women: office clerks, general 80.5 in 100 women; the whole office and administrative support group 70.5 (US BLS CPS 2025, table 11)
       meets="need:safety+.05 res:money+.05 res:time-.1 need:autonomy-.03",
       ages=(16, 75), share=.3,   # estimate: clerical and admin work is one of the largest job groups
       say="an office worker",
       gained="'a job interview', then 'your first full-time job': a desk, a login and a lanyard",
       lost="'new technology changes your job', 'a wave of layoffs at work', a move up",
       needs="[school-leaving certificate] in most offices"),
  dict(name="nurse", kind="career", sector="public", role="women", sphere="care", face="care.W", ways="W G",   # role=women: registered nurses 87.3, nurse practitioners 90.5 in 100 women (US BLS CPS 2025, table 11)
       meets="need:meaning+.1 need:belonging+.05 res:money+.05 res:time-.1 res:health-.05",
       ages=(20, 67), share=.03,   # US: over 3 million registered nurses in a workforce near 160 million (BLS);
                                   # .03 counts those who leave nursing
       say="a nurse",
       gained="a nursing degree and the registration exam, then 'a new job at last' on a ward",
       lost="retirement, 'burnout', or being struck off (the skill stays)",
       needs="[professional registration]; 'learned a skill' several times"),
  dict(name="teacher", kind="career", sector="public", role="women", sphere="learn", face="learn.W", ways="W U",   # role=women: preschool and kindergarten 97.1, elementary and middle 79.2, special education 84.7, secondary 56.5 in 100 women: about 78 over the four (US BLS CPS 2025, table 11); OECD about 7 in 10 across levels
       profiles=[("W U", "Teaches the syllabus well, keeps good order, and knows every child's progress."),   # Stage pack ask
                 ("R G", "Runs the school play and the trips, and the children remember them for life."),   # (P13, 2026-10-07)
                 ("B", "Wants results, the inspection and the head's job.")],
       meets="need:meaning+.1 need:competence+.05 res:money+.05 res:time-.1",
       ages=(21, 75), share=.04,   # estimate: teachers are 2 to 3 workers in 100, and many leave within five years
       say="a teacher",
       gained="a degree and a teaching qualification, then a first class of thirty on a Monday in September",
       lost="retirement, 'burnout', a move into another line of work",
       needs="[graduate]; [professional registration]"),
  dict(name="electrician", kind="career", sector="industry", role="men", sphere="prod", face="prod.U", ways="U",   # role=men: electricians 3.5 in 100 women (US BLS CPS 2025, table 11)
       meets="need:competence+.1 need:safety+.03 res:money+.08 res:time-.08",
       ages=(16, 70), share=.015,   # estimate: about 1 worker in 100 is an electrician
       say="an electrician",
       gained="an apprenticeship, then 'earning a qualification' and a trade ticket",
       lost="retirement, an injury, a slump in building work",
       needs="[apprentice] first; [trade ticket]; 'learned a skill' several times"),
  dict(name="shop owner", kind="career", sector="services", sphere="comm", face="comm.G", ways="B G",
       meets="need:autonomy+.1 need:belonging+.05 need:safety-.05 res:money+.05 res:time-.15",
       ages=(18, 80), share=.04,   # estimate
       say="a shopkeeper",
       gained="'a chance to start a business of your own': savings or a loan, and a lease signed on a high street",
       lost="'financial ruin', 'a recession', selling up, handing the keys to a child",
       needs="[savings] or a loan; often a [family business]"),
  dict(name="soldier", kind="career", sector="public", role="men", sphere="prot", face="prot.R", ways="W R",   # role=men: women about 18 in 100 of US active-duty forces (Department of Defense Demographics Profile 2023) and about 12 in 100 across NATO armed forces (NATO 2019); the CPS counts civilians only
       meets="need:belonging+.1 need:meaning+.05 res:money+.03 res:freedom-.15 res:health-.05",
       ages=(16, 55), share=.05,   # about 6 to 7 US adults in 100 are veterans (VA); fewer in most rich countries
       say="a soldier",
       gained="signing up after school, then basic training; in some lives 'war comes'",
       lost="the end of a term of service, an injury, discharge",
       needs="age 16 to 18 or more, fitness, no serious record"),
  dict(name="farmer", kind="career", sector="farm", sphere="prod", face="prod.G", ways="G B",
       meets="need:autonomy+.08 need:meaning+.05 res:money+.02 res:time-.15 res:health+.02",
       ages=(14, 85), share=.015,   # farming is 1 to 2 jobs in 100 in most rich countries (OECD)
       say="a farmer",
       gained="growing up on a farm and staying, or 'a chance to change everything' and a field bought at auction",
       lost="a run of bad years, selling up, handing on to a child",
       needs="[plot of land], usually a family farm"),
  # v22.4: three green everyday entry jobs (Packs, chroma-packs/notes/v22.4-green-entries-for-library.md): green-led lives
  # had no first job of their own and mostly landed on [shop assistant]. No role= yet: grounds work is mostly men in the
  # sources Packs recalls, but that figure is unchecked; farm work and animal care are mixed.
  dict(name="gardener or groundskeeper", kind="career", sector="services", sphere="prod", face="prod.G", ways="G U",
       profiles=[("G U", "Knows what each bed and tree needs and works with the seasons, not against them."),
                 ("W", "Keeps the park, the school field and the churchyard tidy and safe for everyone.")],
       meets="need:autonomy+.05 need:meaning+.05 res:health+.03 res:money+.02 res:time-.08",
       ages=(16, 75), share=.03,   # estimate: grounds and garden work is about 1 job in 100 at any time (US BLS grounds
                                   # maintenance workers, about 1.2 million), with many short seasons
       say="a gardener",
       gained="a summer on the council's parks crew, a landscaper who needs a pair of hands, a school's or a big "
              "house's grounds; [growing food] or [knowing the woods] help",
       lost="the season ending, a bad back, the contract going to a cheaper firm, a steadier job",
       needs="age 16 or more"),
  dict(name="farm hand", kind="career", sector="farm", sphere="prod", face="prod.G", ways="G R",
       profiles=[("G R", "Out in all weathers with the stock and the machines, and would not swap it for a desk."),
                 ("B", "Takes the long hours and the cash in hand while saving for something of their own.")],
       meets="need:autonomy+.03 need:belonging+.03 res:health+.02 res:money+.02 res:time-.12",
       ages=(14, 70), share=.03,   # estimate: farm work is 1 to 2 jobs in 100 in rich countries (OECD), and many more
                                   # lives do a season or two of it (harvest, lambing, a neighbour's farm)
       say="a farm hand",
       gained="growing up near farms, a harvest job at sixteen, a neighbour short-handed at lambing; [handling "
              "animals] and a [driving licence] help",
       lost="the season ending, the farm selling up or mechanising, an injury, a move to town",
       needs="age 14 or more for holiday work"),
  dict(name="animal care worker", kind="career", sector="services", sphere="care", face="care.G", ways="G W",
       profiles=[("G W", "Feeds, cleans and settles the animals no one else wants, and keeps going on hard days."),
                 ("U", "Learns each animal's signs and the vet's methods, and is the one who spots trouble first.")],
       meets="need:meaning+.08 need:belonging+.03 res:money+.01 res:time-.08 res:health-.02",
       ages=(16, 70), share=.02,   # estimate: kennels, catteries, shelters, stables and a vet's assistants (US BLS
                                   # animal caretakers and veterinary assistants, about 0.4 million together)
       say="an animal care worker",
       gained="[handling animals], weekends at the shelter as an [animal-shelter campaigner], a kennel or a stable "
              "that needs someone, a vet's practice taking on an assistant",
       lost="low pay, the shelter's funding ending, a bite or a bad back, a move into nursing or a vet's training",
       needs="age 16 or more; [handling animals] or real time with animals helps a lot"),
  dict(name="software developer", kind="career", sector="knowledge", role="men", sphere="prod", face="prod.U", ways="U R",   # role=men: software developers 20.3 in 100 women (US BLS CPS 2025, table 11)
       meets="need:competence+.1 need:autonomy+.05 res:money+.1 res:time-.08 res:health-.03",
       ages=(16, 70), share=.03,   # estimate: software work is 2 to 3 jobs in 100
       say="a software developer",
       gained="a degree, or a stubborn year teaching themselves, then 'a job interview' with a coding test",
       lost="'a wave of layoffs at work', 'burnout', a move into management",
       needs="[writing code]"),
  dict(name="shift manager", kind="career", sector="services", ways="W B",
       meets="need:competence+.05 need:autonomy+.03 need:belonging-.03 res:money+.05 res:time-.12",
       ages=(17, 67), share=.15,   # estimate: many shop, café and warehouse workers are made supervisors at some point
       say="a shift manager",
       gained="'a promotion is open' after a year of turning up: the keys, the rota and the blame",
       lost="a move up or out, 'a wave of layoffs at work', asking to step back",
       needs="[reliable record]; a year or more in the job"),
  dict(name="police officer", kind="career", sector="public", role="men", sphere="prot", face="prot.W", ways="W B",   # role=men: police officers 16.4 in 100 women (US BLS CPS 2025, table 11)
       meets="need:meaning+.05 need:safety+.03 res:money+.05 res:time-.12 res:health-.05 res:ties-.03",
       ages=(18, 60), share=.01,   # estimate: police are about 1 worker in 200
       say="a police officer",
       gained="an application, a fitness test and months at training college",
       lost="retirement at 55 to 60, an injury, a complaint upheld",
       needs="not [someone with a record]; age 18 or more"),
  dict(name="cook", kind="career", sector="services", ways="R G",
       meets="need:competence+.05 need:belonging+.05 res:money+.03 res:time-.12 res:health-.05",
       ages=(16, 70), share=.08,   # estimate
       say="a cook",
       gained="starting as a kitchen porter, or 'learning to cook for yourself' taken much further",
       lost="burns and long nights, a kitchen that closes, opening a place of one's own",
       needs="[cooking for a crowd] helps"),
  dict(name="delivery driver", kind="career", sector="services", role="men", sphere="prod", face="prod.B", ways="R B",   # role=men: couriers and messengers 28.7 in 100 women (US BLS CPS 2025, table 11); driver/sales workers and truck drivers about 7 in 100 (US BLS CPS, recent years)
       meets="need:autonomy+.05 need:belonging-.03 res:money+.05 res:time-.12 res:health-.03",
       ages=(18, 78), share=.06,   # estimate
       say="a delivery driver",
       gained="an app or a depot that needs drivers this week",
       lost="losing the licence, the van breaking down, a better job",
       needs="[driving licence]"),
  dict(name="builder", kind="career", sector="industry", role="men", sphere="prod", face="prod.R", ways="U R",   # role=men: construction laborers 4.7, carpenters 3.1 in 100 women (US BLS CPS 2025, table 11)
       meets="need:competence+.08 res:money+.05 res:time-.1 res:health-.05",
       ages=(16, 67), share=.06,   # estimate: construction is 6 to 7 jobs in 100 in rich countries
       say="a builder",
       gained="labouring for a cousin's firm, an apprenticeship, word of mouth",
       lost="a bad back, a building slump, retirement",
       needs="fitness; [building trade] for the skilled end"),
  dict(name="factory worker", kind="career", sector="industry", sphere="prod", face="prod.W", ways="W U",
       meets="need:safety+.03 need:belonging+.05 need:autonomy-.05 res:money+.05 res:time-.12 res:health-.03",
       ages=(16, 67), share=.12,   # estimate: manufacturing is about 1 job in 10 in rich countries
       say="a factory worker",
       gained="an agency placement turned into a contract; a shift pattern pinned to the board",
       lost="'a wave of layoffs at work', a plant that moves abroad, an injury",
       needs="age 16 or more"),
  dict(name="salesperson", kind="career", sector="services", sphere="comm", face="comm.B", ways="B",
       meets="need:competence+.05 need:autonomy+.03 need:safety-.05 res:money+.05 res:time-.1",
       ages=(17, 80), share=.08,   # estimate
       say="a salesperson",
       gained="'a job interview' where hunger counts for more than a degree, and a target for the first month",
       lost="a bad quarter, a better offer, 'burnout'",
       needs="[selling] helps"),
  dict(name="accountant", kind="career", sector="knowledge", sphere="comm", face="comm.U", ways="U B",
       meets="need:competence+.08 need:safety+.05 res:money+.08 res:time-.1",
       ages=(21, 80), share=.02,   # estimate: accountants and auditors are about 1 worker in 100
       say="an accountant",
       gained="a trainee post and years of evening exams, then 'earning a qualification'",
       lost="retirement, 'new technology changes your job', a move into running a firm",
       needs="[bookkeeping]; often [graduate]"),
  dict(name="estate agent", kind="career", sector="services", sphere="comm", face="comm.B", ways="B R",
       meets="need:competence+.03 need:autonomy+.03 need:safety-.05 res:money+.08 res:time-.12",
       ages=(18, 80), share=.01,   # estimate
       say="an estate agent",
       gained="'a job interview' at a high-street agency, and a car and a phone on the first day",
       lost="'a recession', a slow market, weekend viewings that wear them out",
       needs="[driving licence]; [selling] helps"),
  dict(name="founder of a firm", kind="career", sector="services", sphere="prod", face="prod.B", ways="U B R",
       meets="need:autonomy+.1 need:competence+.05 need:safety-.08 res:money+.05 res:time-.15 res:health-.03",
       ages=(18, 80), share=.03,   # estimate: someone who starts a firm that takes on staff; a few people in 100
       say="the founder of a firm",
       gained="'a chance to start a business of your own' or 'a friend wants to start a project with you', "
              "then a first hire",
       lost="'financial ruin', selling the firm, being pushed out by the backers",
       needs="[savings] or backers; 'took a wild risk'"),
  dict(name="head chef", kind="career", sector="services", ways="B R",
       meets="need:competence+.08 need:autonomy+.05 res:money+.05 res:time-.15 res:health-.05",
       ages=(22, 70), share=.015,   # estimate
       say="a head chef",
       gained="years as a [cook], then 'a promotion is open' when the old head chef walks out",
       lost="a kitchen that closes, 'burnout', a row with the owner",
       needs="[cook] for years"),
  dict(name="apprentice", kind="career", sector="industry", sphere="prod", face="prod.G", ways="U G",
       meets="need:competence+.08 need:belonging+.05 need:autonomy-.05 res:money-.03 res:time-.1",
       ages=(15, 30), share=.12,   # estimate: about 1 young person in 10 in the UK; over half in Germany or Switzerland
       say="an apprentice",
       gained="a place with a firm after school, and a master who shows them; 'a teacher or coach who believes in you'",
       lost="qualifying (the trade's own title follows), dropping out, the firm folding",
       needs="age 15 or 16 or more"),
]

