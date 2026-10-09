# odds: optional (engine 08:55). Skill, standing and bond perks give better odds to acts in their ways; access perks
# (credentials and assets: a licence, a passport, a car, savings, a house) carry odds=0 and work only through
# requires: on specific acts, which the Library's act pass adds.
# Chroma Library: titles and perks for modern Earth (draft, Library thread, 2026-10-05).
# Asked for by Emren (08:05: "do we have enough perks and titles to increase the richness of one life's depth. Is it
# realistic numbers?"). Plan in chroma-library/perks-titles-plan.md. Written to the engine's format
# (chroma-engine/perks-titles-format.md, 08:15). Plain data: nothing is imported, nothing runs. Modern Earth only; the
# tribal and magic worlds get their own catalogues later, so there is no worlds field.
#
# The file is built as TITLES = [] and PERKS = [], with one "+= [...]" block per kind, so it stays valid at every step.
#
# TITLES: a role or status other people recognise, held for a stretch of life. A title of one of the five commitment
# kinds refines that commitment (holding "nurse" means holding a career with the nurse's colors as its profile); one
# title per commitment kind at a time. Statuses stand outside the commitments, and a person may hold any number.
#   name     the title as a short phrase, the key acts use (title:, drops:, requires:)
#   kind     career | partner | children | community | faith | status
#   ways     the colors the role expects of its holder and rewards, as letters ("W G"); it becomes the commitment's
#            profile. Each letter counts 1/len in the balance (a pair .5 each, a triad 1/3 each). Every status has
#            ways="": a status is a fact about a life (a record, a divorce, a degree), not a role with expectations,
#            and only commitment-kind titles become a commitment's profile. A status works through meets alone
#   meets    what holding it gives or costs while held, in the engine's base: syntax: need:<safety|belonging|autonomy|
#            competence|meaning>+.x and res:<money|time|health|ties|freedom>+.x; sizes .02 to .15. Written as the
#            title's own effect on top of what its commitment kind already meets (library.py COMMITMENTS). Since one
#            title per commitment kind is held at a time, a later title of the same kind (parent of three, team
#            captain, deacon) replaces the earlier one and carries its full effect; statuses add up
#   ages     (youngest, oldest) a person can hold it
#   share    the share of people in a modern rich country who ever hold it in their life, 0 to 1. The sum over TITLES
#            is the number of titles an average life holds over its course (target 10 to 20). A named source follows
#            where a well-known figure exists; anything else says "estimate"
#   say      how the story names the person ("a nurse")
#   lasts    statuses only: "life", or the years it lasts by itself before it fades (newcomer 2)
#   gained   plain words: how one comes to hold it. Situations from earth.md and the engine's history marks are in
#            single quotes ('a new job at last', 'learned a skill'); titles and perks of this file in brackets ([nurse])
#   lost     plain words: what ends it
#   needs    plain words: what must come first (a title, a perk, a history mark, an age, money)
#   profiles optional (engine 12:45): two or three equally valid ways to hold the title, [("W U", "words"), ...]; ways
#            is the first profile. A person holds the profile that fits them best and may move to another as their
#            colors drift ("reshaped", never a new title). In the balance each profile counts 1, split over its letters
#   refines  optional (engine 12:45): a facet, held on top of the title it names (newlywed on [wife or husband]); it
#            takes no slot of its kind and ends with that title. Several titles with ";" (engine 15:00): the facet sits
#            on any of them and ends when none is held
#   turning  optional: Emren's "ordinary turning point" for the title, the seed of a moment only its holders meet
#   sector   careers only (outer world, chroma-engine/world-fields.md, 2026-10-07): farm, industry, services, knowledge
#            or public. The economy and automation reach a job through its sector, and the state budget moves the
#            public ones. Jobs mostly paid from the public purse in a rich democracy (nurse, teacher, care worker,
#            physician, soldier, postal worker) are public; transport and retail are services; trades are industry
#
# PERKS: something a person can do or has access to that changes their odds or opens options. Emren's lifecycle:
# eligible, acquired, suspended, lost, retired, regained. Losing access keeps the skill, which then fades by
# skill_half: a struck-off nurse still knows nursing. Temperament and discipline are the engine's own learned traits,
# so they are not perks; a learned way that is a concrete skill (calming people down, public speaking) is a skill.
#   name       the perk as a short phrase, the key acts use (grants:, takes:, suspends:, requires:)
#   kind       skill | credential | standing | bond | asset
#   ways       the colors of the acts it helps, as letters ("R G"); counted 1/len each in the balance
#   odds       how much better acts in those ways go while the perk lasts, .02 to .1
#   skill_half years for what it taught to fade by half once access is gone or it goes unused; None when nothing is
#              left to fade (most assets: money spent is gone; a citizenship is never unlearned)
#   retires    an age at which it ends by itself, or None (body perks end when health makes them impossible)
#   ages       (youngest, oldest) a person can hold it
#   share      the share of people who ever hold it (target sum 15 to 30), sourced or "estimate" as for titles
#   say        a short phrase for the story ("can drive")
#   gained, lost, needs   plain words, as for titles
#
# Balance (checked by check_perks_titles.py): over the commitment-kind TITLES (career, partner, children, community,
# faith; statuses carry no colors and stay out of it), and separately over PERKS, the ways letters summed per color
# (1/len each) are within 3% of each other, and every commitment kind and every perk kind holds all five colors.
# Singles, ally pairs, enemy pairs and triads all appear. Every color's entries hold discipline, care, ambition,
# curiosity and freedom in its own way: the boxer's training is Red discipline, the single parent's provision is Black
# care, the farmer's growing herd is Green ambition, the stepparent's slow patience is Blue care, the union rep's
# stand is White freedom.
#
# Realism groups (shares that interact):
#   - Nested titles: [veteran] and [has killed in war] come only after [soldier]; [ex-prisoner] only with
#     [someone with a record]; [parent of three or more], [single parent] and [grandparent] after [mother or father];
#     [partner of many years] after [living together] or [wife or husband]; [team captain] after [on the team]. Each is
#     its own recognised title, so its share counts again.
#   - One at a time: the career titles are held one after another (12.7 jobs from 18 to 56 for Americans born 1957 to
#     1964, US BLS NLSY79, 2023, many of them in the same few kinds of work), so their shares add up to about two
#     recognisable kinds of work per life, as listed here; the partner titles are a sequence (sweetheart, engaged,
#     living together, married, many years), so their shares add past 1.
#   - One per kind at a time: [on the team], [scout or guide] and [prefect] all take the child's one community slot,
#     and [regular worshipper], [activist in a cause] and [party member] the one faith slot (an engine question,
#     listed in perks_titles.md).
#   - Both at once: [newcomer] (new in town, fades in two years) and [immigrant] (for life).
# Statuses the engine grants itself (widowed, retiree, newcomer) are named here so the story uses these words; each
# carries the comment "granted by the engine".
#
# Safety (Emren's limits): dark statuses are named in plain words (a record, prison, a gang, homelessness, killing in
# war); nothing touches sexual violence, nothing makes harming children a role or a skill, nothing is graphic, and no
# entry moralises.

TITLES = []
PERKS = []

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

# ---------- partner: a sequence over a life, so the shares add past 1
TITLES += [
  dict(name="girlfriend or boyfriend", kind="partner", ways="R",
       meets="need:belonging+.1 need:autonomy-.02 res:ties+.03 res:time-.05",
       ages=(12, 110), share=.9,   # estimate: nearly everyone has a sweetheart at some point
       say="someone's sweetheart",
       gained="'falling in love', 'a dating app match', a slow dance at 'a friend's wedding'",
       lost="'a breakup', or the next step: moving in, getting engaged",
       needs="someone who says yes"),
  dict(name="engaged", kind="partner", ways="W R",
       meets="need:belonging+.08 need:meaning+.05 need:safety+.03 res:money-.03",
       ages=(16, 110), share=.55,   # estimate: most first marriages follow an engagement
       say="engaged to be married",
       gained="a proposal, accepted, often a year or two after 'moving in with a partner'",
       lost="'getting married', or calling it off",
       needs="[girlfriend or boyfriend]"),
  dict(name="living together", kind="partner", ways="U B",
       meets="need:belonging+.08 need:safety+.05 need:autonomy-.05 res:money+.05 res:time-.05",
       ages=(17, 110), share=.65,   # US: close to 6 in 10 women aged 18 to 44 have lived with a partner (NSFG,
                                    # 2010s); more by the end of life
       say="living with a partner",
       gained="'moving in with a partner': two names on a lease and one set of keys too few",
       lost="'a breakup', or 'getting married'",
       needs="[girlfriend or boyfriend]"),
  dict(name="wife or husband", kind="partner", ways="W G",
       meets="need:belonging+.1 need:safety+.08 need:autonomy-.05 res:ties+.05 res:money+.03",
       ages=(16, 110), share=.7,   # estimate: about 7 in 10 people in rich countries marry at least once, fewer in
                                   # younger cohorts
       say="married",
       gained="'getting married', in a registry office or a hall full of cousins",
       lost="'divorce after twenty years', a shorter marriage ended in court, or 'your partner dies'",
       needs="usually [engaged]; a partner willing"),
  dict(name="partner of many years", kind="partner", ways="U G",
       meets="need:belonging+.1 need:safety+.1 need:meaning+.05 need:autonomy-.03 res:ties+.05",
       ages=(40, 110), share=.4,   # estimate: about half of first marriages reach 25 years, plus long unmarried couples
       say="together for many years",
       gained="'twenty-five years together', reached one ordinary day at a time",
       lost="divorce, or 'your partner dies'",
       needs="[wife or husband] or [living together] for twenty years or more; 'kept your word'"),
  dict(name="married again", kind="partner", ways="U R",
       meets="need:belonging+.1 need:safety+.08 need:autonomy-.03 res:ties+.05 res:money+.03",
       ages=(25, 110), share=.15,   # estimate: about 1 married American in 5 has been married before
       say="married again",
       gained="'a late love' or 'an old flame gets in touch' after a divorce or a death; a smaller, surer wedding",
       lost="a second divorce, a death",
       needs="[divorced] or [widowed]"),
]

# ---------- children: nested (three or more, single parent, grandparent come after a first child)
TITLES += [
  dict(name="mother or father", kind="children", ways="G W",
       meets="need:meaning+.12 need:belonging+.05 need:autonomy-.05 res:time-.15 res:money-.08 res:health-.03",
       ages=(14, 110), share=.8,   # 86% of US women aged 40 to 44 are mothers (Pew 2018); fewer men are fathers
       say="a parent",
       gained="'a child is born', or 'a baby on the way, planned or not'",
       lost="never quite; the daily duties ease when 'the children leave home'",
       needs="a partner, usually; or adoption"),
  dict(name="parent of three or more", kind="children", ways="G R",
       meets="need:meaning+.12 need:belonging+.08 need:autonomy-.08 res:ties+.05 res:time-.15 res:money-.12",
       ages=(20, 110), share=.22,   # about 4 US mothers in 10 have three or more (Pew 2015); far fewer in most of
                                    # Europe; estimate
       say="a parent of three",
       gained="'a child is born' for the third time, and a bigger car",
       lost="never; the house goes quiet when 'the children leave home'",
       needs="[mother or father]"),
  dict(name="single parent", kind="children", ways="B G",
       meets="need:meaning+.12 need:autonomy+.03 need:safety-.05 res:time-.15 res:money-.12 res:health-.05",
       ages=(16, 70), share=.2,   # about 1 family with children in 4 has one parent at a time (UK ONS); estimate
                                  # for ever being one
       say="a single parent",
       gained="'a breakup' or 'your partner dies' with a child at home, or a child raised alone from the start",
       lost="a new partner moving in, or the youngest growing up and leaving",
       needs="[mother or father]"),
  dict(name="stepparent", kind="children", ways="U G",
       meets="need:meaning+.05 need:belonging+.03 need:safety-.03 res:time-.08 res:money-.05",
       ages=(20, 110), share=.12,   # about 13% of US adults have a stepchild (Pew 2011)
       say="a stepparent",
       gained="'moving in with a partner' or 'getting married' to someone who already has children",
       lost="a divorce, though the bond can outlast it",
       needs="a partner with children"),
  dict(name="foster parent", kind="children", ways="W",
       meets="need:meaning+.12 need:safety-.03 res:ties+.03 res:time-.15 res:money-.03",
       ages=(25, 75), share=.015,   # estimate: well under 1 household in 100 fosters at any time
       say="a foster parent",
       gained="'you take in a child who needs a home', after training, checks and a social worker's visit",
       lost="children moving on, retirement, stopping after a hard placement",
       needs="age 21 to 25 or more, a spare room, a background check ([cleared to work with children])"),
  dict(name="adoptive parent", kind="children", ways="W U",
       meets="need:meaning+.12 need:belonging+.05 res:time-.12 res:money-.08",
       ages=(25, 110), share=.02,   # about 2 children in 100 in the US are adopted (US Census 2010); estimate
       say="an adoptive parent",
       gained="two years of forms, assessments and waiting, then a phone call; 'you take in a child who needs a home'",
       lost="never; it is for life",
       needs="age 21 or more, a stable home, a background check"),
  dict(name="grandparent", kind="children", ways="G R U",
       meets="need:meaning+.08 need:belonging+.08 res:ties+.05 res:time-.03",
       ages=(35, 110), share=.6,   # estimate: most people who live past 65 become grandparents
       say="a grandparent",
       gained="'your first grandchild'",
       lost="never",
       needs="[mother or father], and a child who has a child"),
]

# ---------- community: one at a time ([team captain] follows [on the team])
TITLES += [
  dict(name="on the team", kind="community", sphere="gather", face="gather.R", ways="R G",
       meets="need:belonging+.08 need:competence+.03 res:health+.05 res:time-.08",
       ages=(7, 60), share=.5,   # estimate: about half of young people play on an organised team at some point
       say="on the team",
       gained="'tryouts for the team', 'sports day', 'a band or a sport that takes over your life'",
       lost="being dropped, an injury, leaving school, growing out of it",
       needs="turning up on Saturday mornings"),
  dict(name="scout or guide", kind="community", sphere="learn", face="learn.G", ways="W G",
       meets="need:belonging+.08 need:competence+.03 res:time-.05",
       ages=(6, 18), share=.2,   # estimate
       say="a scout",
       gained="a friend brings them along to the hall on a Tuesday; 'summer camp'",
       lost="growing out of it, 'the family moves to a new town'",
       needs="age 6 or more"),
  dict(name="prefect", kind="community", sphere="learn", face="learn.W", ways="W U",
       meets="need:competence+.03 need:belonging+.03 need:meaning+.03 res:time-.03",
       ages=(10, 18), share=.1,   # estimate
       say="a prefect",
       gained="'a teacher offers you a role of responsibility', 'you are picked for something special'",
       lost="leaving school, or losing the badge for breaking the rules",
       needs="[teachers' favourite]"),
  dict(name="team captain", kind="community", sphere="gather", face="gather.R", ways="R B",
       meets="need:belonging+.08 need:competence+.05 need:meaning+.03 res:health+.05 res:time-.1",
       ages=(10, 50), share=.12,   # estimate
       say="the captain",
       gained="picked by the coach or voted in by the team after 'tryouts for the team'",
       lost="a loss of form or nerve, a new captain, leaving the team",
       needs="[on the team]"),
  dict(name="neighbourhood volunteer", kind="community", sphere="gather", face="gather.G", ways="G W",
       meets="need:belonging+.08 need:meaning+.05 res:ties+.05 res:time-.05",
       ages=(12, 100), share=.35,   # about 1 adult in 4 in England volunteers formally at least once a year
                                    # (Community Life Survey); estimate for holding it as a role
       say="a volunteer",
       gained="'a volunteer drive in your neighbourhood', 'a young neighbour needs help'",
       lost="a busier job, a move, a falling-out with the organisers",
       needs="nothing but a free Saturday"),
  dict(name="union rep", kind="community", sphere="prod", face="prod.W", ways="W R",
       meets="need:meaning+.05 need:belonging+.05 need:safety-.02 res:time-.05",
       ages=(20, 67), share=.03,   # estimate
       say="the union rep",
       gained="elected by workmates after 'a wave of layoffs at work', or 'they ask you to lead because you stood up once'",
       lost="losing the vote, leaving the job, being eased out",
       needs="a job with a union; 'defied an authority' helps"),
  dict(name="local councillor", kind="community", sphere="rule", ways="W B",
       profiles=[("W B", "Serves the town through its rules and knows how the council's power works."),
                 ("R G", "Fights for the street they grew up on, loud and stubborn."),   # third and second: packs
                 ("U B", "Reads every planning paper and catches what the officers missed.")],   # thread 22:20, Library
       meets="need:meaning+.05 need:competence+.03 need:safety-.02 res:ties+.05 res:time-.1",
       ages=(18, 90), share=.01,   # estimate: about 1 adult in 500 in England sits on a council, parish ones included
       say="a councillor",
       gained="a campaign on doorsteps and a vote; 'your town faces a change you could fight'",
       lost="losing the next election, a scandal, standing down",
       needs="[good name in town]; age 18 or more"),
  dict(name="youth coach", kind="community", sphere="learn", face="learn.R", ways="R U",
       meets="need:meaning+.05 need:belonging+.05 res:time-.08",
       ages=(18, 80), share=.06,   # estimate
       say="a coach",
       gained="the old coach quits and a parent on the touchline is asked to take over",
       lost="their own children growing out of the team, 'burnout'",
       needs="[on the team] once; a [coaching badge] in most clubs"),
  dict(name="residents' committee member", kind="community", sphere="rule", face="rule.G", ways="B G",
       meets="need:belonging+.05 need:safety+.03 need:autonomy+.02 res:time-.05",
       ages=(25, 100), share=.05,   # estimate
       say="on the residents' committee",
       gained="'a seat on the residents' committee', often after 'break-ins on the street'",
       lost="moving away, a row at the meeting, standing down",
       needs="[homeowner] or a long tenancy"),
  dict(name="club treasurer", kind="community", sphere="gather", face="gather.B", ways="U B",
       meets="need:competence+.05 need:belonging+.05 res:ties+.03 res:time-.05",
       ages=(18, 90), share=.05,   # estimate: sports clubs, choirs, allotment societies and the like
       say="the club treasurer",
       gained="'the club or congregation asks you to lead', and nobody else will take the books",
       lost="an audit that goes badly, standing down at the yearly meeting, a move",
       needs="[bookkeeping]; [reliable record]"),
  dict(name="club member", kind="community", ways="W R",
       meets="need:belonging+.08 need:competence+.03 res:ties+.05 res:time-.05",
       ages=(16, 100), share=.4,   # estimate: a grown-up's first club, the commonest first community title for adults
                                   # (engine 10:15: neighbourhood volunteer took most community starts)
       say="a member of a club",
       gained="a friend's invitation to a running club, a choir, a five-a-side side, a chess club or a book group",
       lost="a move, a busier job or a new baby, a falling-out, the club folding",
       needs="a free evening a week"),
  dict(name="in a street gang", kind="community", ways="B R G",
       meets="need:belonging+.1 need:autonomy+.02 need:safety-.08 res:freedom-.05 res:health-.05",
       ages=(12, 30), share=.03,   # estimate: US youth surveys find several teenagers in 100 who were ever in a gang;
                                   # fewer in most rich countries
       say="in a gang",
       gained="drifting in through older friends on the estate after 'a fight after school' or 'money runs out at home'",
       lost="growing up, moving away, prison, a death that changes everything",
       needs="age 12 or more"),
]

# ---------- faith: a religion, an ideology or a cause, held one at a time
TITLES += [
  dict(name="regular worshipper", kind="faith", sphere="faith", face="faith.W", ways="W G",
       meets="need:meaning+.08 need:belonging+.08 res:ties+.05 res:time-.03",
       ages=(5, 110), share=.3,    # estimate: about 3 Americans in 10 attend weekly (Gallup), under 1 Briton in 10;
                                   # more hold a stretch of it over a life
       say="a regular at church, mosque, temple or synagogue",
       gained="raised in it from 'starting school', or 'welcomed into a community' later in life",
       lost="drifting away, 'a scandal in the congregation', a move",
       needs="a faith held"),
  dict(name="believer on the big days", kind="faith", sphere="faith", face="faith.G", ways="U B G",
       meets="need:belonging+.05 need:meaning+.03 res:ties+.03",
       ages=(5, 110), share=.4,   # estimate: in most rich countries more people are raised in a faith and keep its
                                  # feasts, weddings and funerals than attend services (engine 10:15 asked for them)
       say="a believer on the big days",
       gained="raised in a faith at home, then drifting from the services in the teenage years while keeping the feasts",
       lost="finding a real faith ([regular worshipper], [convert]) or letting the last customs go",
       needs="raised in a faith"),
  dict(name="deacon or elder", kind="faith", sphere="faith", face="faith.W", ways="W B",
       meets="need:meaning+.1 need:belonging+.08 res:ties+.05 res:time-.08",
       ages=(30, 100), share=.03,   # estimate
       say="an elder of the congregation",
       gained="'the club or congregation asks you to lead'",
       lost="stepping down, a split in the congregation, 'a scandal in the congregation'",
       needs="[regular worshipper] for years; [known face at worship]"),
  dict(name="activist in a cause", kind="faith", sphere="rule", face="rule.R", ways="R G",
       meets="need:meaning+.1 need:belonging+.05 need:safety-.03 res:time-.08 res:freedom-.02",
       ages=(14, 100), share=.1,   # estimate
       say="an activist",
       gained="'a protest in your city', 'a sense of injustice', 'a protest to save the local hospital'",
       lost="'a cause you fought for wins', 'burnout', a job that takes every evening",
       needs="a cause that matters to them"),
  dict(name="party member", kind="faith", sphere="rule", face="rule.B", ways="B U",
       profiles=[("B U", "Joins for influence and a clear idea of how the country should run."),
                 ("W G", "Belongs to the party as to a family and a duty."),   # packs thread 22:20 (Politics pack)
                 ("R", "Joins for the fire of the cause.")],
       meets="need:meaning+.05 need:belonging+.05 res:ties+.03 res:time-.03",
       ages=(16, 100), share=.06,   # estimate: under 2 adults in 100 belong to a party at a time in most of Europe
       say="a party member",
       gained="'a bitter election', or a friend's invitation to a branch meeting above a pub",
       lost="a quarrel with the leadership, letting the membership lapse",
       needs="age 14 to 16 or more"),
  dict(name="convert", kind="faith", sphere="faith", face="faith.B", ways="U B",
       meets="need:meaning+.1 need:belonging+.05 res:ties-.03",
       ages=(14, 110), share=.08,   # about a third of US adults have changed religion, most of them to none (Pew 2015);
                                   # estimate for joining a new faith
       say="a convert",
       gained="a long search, a partner's faith, 'welcomed into a community'",
       lost="leaving again",
       needs="a faith they were not raised in"),
  dict(name="seeker", kind="faith", sphere="faith", face="faith.U", ways="G U",
       meets="need:meaning+.08 need:autonomy+.03 res:time-.03",
       ages=(15, 110), share=.1,   # estimate
       say="a seeker",
       gained="'a sleepless night: is this all there is?', a meditation class, 'awe' on a mountain",
       lost="settling into one faith, or giving the search up",
       needs="nothing"),
]

# ---------- status: any number at once, no colors (ways=""), out of the color balance; lasts is "life" or the years
# a status lasts by itself
TITLES += [
  dict(name="graduate", kind="status", ways="",
       meets="need:competence+.05 res:money+.05", lasts="life",
       ages=(20, 110), share=.4,   # about 4 adults in 10 aged 25 to 64 hold a tertiary degree (OECD average)
       say="a graduate",
       gained="three or four years of study, 'exams are coming' every spring, then 'earning a qualification'",
       lost="never",
       needs="'you win a scholarship or a place'; [school-leaving certificate]"),
  dict(name="veteran", kind="status", ways="",
       meets="need:belonging+.03 need:meaning+.03 res:health-.03", lasts="life",
       ages=(19, 110), share=.05,   # as [soldier]: nearly everyone who serves becomes a veteran
       say="a veteran",
       gained="leaving the forces after a term of service",
       lost="never",
       needs="[soldier]"),
  dict(name="has killed in war", kind="status", ways="",
       meets="need:safety-.05 need:meaning-.03 need:belonging+.03 res:health-.05", lasts="life",
       ages=(18, 110), share=.01,   # estimate: few soldiers of rich countries today; many more in the world-war
                                    # generations
       say="a soldier who has killed in war",
       gained="'war comes', and a day under fire",
       lost="never",
       needs="[soldier]"),
  dict(name="has taken a life", kind="status", ways="",   # next batch (Emren 21:00, "By choice, rarely"); granted by the engine
       meets="need:safety-.05 need:meaning-.05 need:belonging-.05 res:ties-.05", lasts="life",
       ages=(16, 110), share=.004,   # estimate: US homicide offending runs about 5 in 100,000 people a year (FBI, BJS), most
                                     # offenders kill once; deaths caused at the wheel and killings in defence add a little
       say="someone who has taken a life",
       gained="a death outside war that the person caused: in defence, in a fight gone wrong, at the wheel, or by choice; "
              "never told in detail",
       lost="never",
       needs="a moment that brings a person there; [someone with a record] follows for about half"),
  dict(name="widowed", kind="status", ways="",   # granted by the engine
       meets="need:belonging-.1 need:safety-.05 need:autonomy+.03 res:ties-.05", lasts="life",
       ages=(18, 110), share=.3,   # estimate: about 4 women in 10 over 65 are widows, far fewer men
       say="a widow or widower",
       gained="'your partner dies'",
       lost="[married again] takes its place in the story, though the loss stays",
       needs="[wife or husband] or [partner of many years]"),
  dict(name="retiree", kind="status", ways="",   # granted by the engine
       meets="need:autonomy+.08 need:competence-.03 need:meaning-.03 res:time+.15 res:money-.05", lasts="life",
       ages=(50, 110), share=.75,   # estimate: most people reach 65, and most who do retire
       say="retired",
       gained="'the first months of retirement', "
              "after 'a party for twenty-five years in the job' that turns into a farewell",
       lost="going back to work",
       needs="a career held for years; a [workplace pension] makes it easier"),
  dict(name="homeowner", kind="status", ways="",
       meets="need:safety+.08 need:autonomy+.05 res:money-.05 res:time-.03", lasts="life",
       ages=(20, 110), share=.7,   # estimate: about 2 households in 3 own their home in the UK and US; more do at
                                   # some point in life
       say="a homeowner",
       gained="'buying a home': a mortgage signed with shaking hands; or 'an unexpected legacy'",
       lost="'losing the home', selling up, 'moving to a smaller home or into care'",
       needs="[savings] for a deposit and [good credit]"),
  dict(name="newcomer", kind="status", ways="",   # granted by the engine
       meets="need:belonging-.08 need:autonomy+.03 res:ties-.08", lasts=2,
       ages=(0, 110), share=.6,   # estimate: most people move to a new town at least once
       say="new in town",
       gained="'the family moves to a new town', or a move for work or love ('moved away')",
       lost="two years of making friends; 'welcomed into a community'",
       needs="a move"),
  dict(name="immigrant", kind="status", ways="",
       meets="need:belonging-.05 need:safety-.03 need:autonomy+.03 res:ties-.08 res:money-.03", lasts="life",
       ages=(0, 110), share=.14,   # foreign-born people are about 14% of the population across rich OECD countries
                                   # (OECD)
       say="an immigrant",
       gained="a visa and a one-way ticket ('moved away'), or the family's move when they were small",
       lost="never; [citizenship] changes what it costs",
       needs="a reason to leave and a country that lets them in"),
  dict(name="someone with a record", kind="status", ways="",
       meets="need:safety-.03 res:freedom-.1 res:money-.03", lasts="life",
       ages=(10, 110), share=.15,   # estimate: UK and US counts of people with any conviction run from about 1 adult
                                    # in 5 to 1 in 3, minor ones included; fewer in much of Europe
       say="someone with a record",
       gained="a conviction: 'a chance to make money on the side, not quite legal' that went wrong, "
              "or 'a night out that gets out of hand'",
       lost="in some countries a minor record is spent after some years; otherwise never",
       needs="an offence and a court"),
  dict(name="ex-prisoner", kind="status", ways="",
       meets="need:belonging-.05 res:freedom-.08 res:ties-.05 res:money-.05", lasts="life",
       ages=(15, 110), share=.02,   # about 3 US adults in 100 have been in prison (Shannon et al. 2017); fewer in
                                    # most of Europe
       say="an ex-prisoner",
       gained="a prison sentence served, and the gate opening one morning",
       lost="never",
       needs="[someone with a record]"),
  dict(name="in recovery", kind="status", ways="",
       meets="need:meaning+.05 need:belonging+.03 need:safety-.03 res:health+.05", lasts="life",
       ages=(14, 110), share=.09,   # about 9% of US adults once had a drink or drug problem and no longer do
                                    # (Kelly et al. 2017)
       say="in recovery",
       gained="after 'an addiction takes hold': a first meeting, a first sober month, then the next",
       lost="a relapse; the title can be taken up again",
       needs="an addiction behind them"),
  dict(name="divorced", kind="status", ways="",
       meets="need:autonomy+.05 need:belonging-.05 res:money-.08 res:ties-.03", lasts="life",
       ages=(18, 110), share=.28,   # about 4 marriages in 10 end in divorce in England and Wales (ONS) and the US
       say="divorced",
       gained="'divorce after twenty years', or a short marriage ended in court",
       lost="never; [married again] sits beside it",
       needs="[wife or husband]"),
  dict(name="eldest child", kind="status", ways="",
       meets="need:meaning+.03 need:competence+.03 need:autonomy-.03 res:time-.03", lasts="life",
       ages=(2, 110), share=.35,   # estimate: in families of two or three, a third to a half of the children are
                                   # the eldest
       say="the eldest child",   # 2026-10-07 (Emren's point 4): "the eldest" alone read like an elder's standing
       gained="a younger brother or sister is born, so the first-born becomes the eldest (from about age 2)",
       lost="never",
       needs="a younger sibling"),
  dict(name="carer for a parent", kind="status", ways="",
       meets="need:meaning+.05 need:belonging+.03 need:autonomy-.08 res:time-.15 res:health-.05 res:money-.05",
       lasts=5,
       ages=(10, 90), share=.25,   # 3 in 5 people in the UK become carers at some point (Carers UK); estimate for
                                   # caring for a parent
       say="a carer",
       gained="'a parent comes to stay for a week' and stays; 'a heart attack or stroke' in the family",
       lost="the parent's death, or the parent 'moving to a smaller home or into care'",
       needs="a parent who needs care"),
  dict(name="homeless", kind="status", ways="",
       meets="need:safety-.15 need:belonging-.08 res:health-.1 res:money-.05", lasts=1,
       ages=(14, 110), share=.05,   # about 7 US adults in 100 have been homeless at some point (Link et al. 1994);
                                    # estimate for rich countries
       say="homeless",
       gained="'losing the home', 'financial ruin', or a family row at sixteen and nowhere to go",
       lost="a flat through the council or a charity; a friend's sofa that turns into a room",
       needs="nowhere to go"),
  dict(name="out of work", kind="status", ways="",
       meets="need:competence-.08 need:meaning-.05 need:safety-.05 res:money-.1 res:time+.1", lasts=2,
       ages=(17, 67), share=.15,   # estimate: out of work for a year or more at some point
       say="out of work",
       gained="'losing your job', then months of 'a job interview' that goes nowhere",
       lost="'a new job at last'",
       needs="losing a job, or never finding one"),
  dict(name="cancer survivor", kind="status", ways="",
       meets="need:meaning+.05 need:safety-.03 res:health-.05", lasts="life",
       ages=(5, 110), share=.2,   # 1 person in 2 gets cancer (Cancer Research UK), and about half survive ten years
       say="a cancer survivor",
       gained="'a frightening diagnosis', months of treatment, then the all-clear",
       lost="never",
       needs="cancer, and treatment that works"),
  dict(name="left the faith", kind="status", ways="",
       meets="need:autonomy+.05 need:belonging-.05 need:meaning-.02 res:ties-.03", lasts="life",
       ages=(12, 110), share=.2,   # nearly 1 US adult in 5 was raised in a religion and now has none (Pew 2015)
       say="someone who left the faith they grew up in",
       gained="a long doubt, a scandal, a new life in a city; 'among the faith you left' tests it",
       lost="coming back",
       needs="a faith in childhood"),
]

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
       gained=("a long training in [counselling] with supervised clients and therapy of their own, then a caseload in "
               "a clinic or a private practice"),
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
       gained="early shifts as a bakery assistant that become responsibility for the bake",
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

# ---------- volume 2, partner, children, community, faith and status (T2-046 to T2-100); facets (refines=) sit on
# the title they refine and take no slot
TITLES += [
  # ---------- partner: facets on [wife or husband], and one partnership of its own kind
  # T2-046
  dict(name="newlywed", kind="partner", ways="R", refines="wife or husband; married again",
       profiles=[("R", "Lives the first stretch of marriage as a joyful, expressive beginning."),
                 ("U", "Learns deliberately how the new shared arrangement actually works."),
                 ("G", "Grows into the wider family that the marriage joins to their own.")],   # third: Library
       meets="need:belonging+.03 need:meaning+.03 res:money-.03 res:time-.02", lasts=2,
       ages=(16, 110), share=.65,   # as [wife or husband] (first marriages): nearly every one begins with this stretch
       say="newly married",
       gained="'getting married', in a registry office or a hall full of cousins; the first year or two after the wedding",
       lost="settling into the ordinary [wife or husband] after a year or two; a separation; 'your partner dies'",
       needs="[wife or husband]; a facet held on top of it, never in its place"),
  # T2-047
  dict(name="caregiving partner", kind="partner", ways="W G", refines="wife or husband; living together; married again; partner of many years; nonromantic life partner",
       profiles=[("W G", "Makes continuing care part of an existing bond and shared life."),
                 ("B", "Protects the partner's agency while maintaining boundaries around their own capacity."),
                 ("R", "Keeps warmth and spontaneity alive in a shared life reshaped by care.")],   # third: Library
       meets="need:meaning+.05 need:belonging+.03 need:autonomy-.03 res:time-.12 res:money-.03 res:health-.03",
       lasts=10,
       ages=(18, 110), share=.15,   # estimate: 3 in 5 people become carers at some point (Carers UK), about 1 family
                                    # carer in 8 cares for a spouse or partner (AARP and NAC 2020), and most couples who
                                    # grow old together see one fall seriously ill; raised from .08 (2026-10-05 17:45)
       say="caring for their partner",
       gained="a partner needs sustained practical support after a stroke, an accident or a long illness, and help "
              "becomes daily care; taken by an act in a moment about a partner falling ill",
       lost="care needs changing, paid care or another arrangement taking over, a separation, 'your partner dies'",
       needs="[wife or husband], a willing partnership on both sides and a real ongoing care responsibility",
       turning="The help that was welcomed last month now feels intrusive. Love has to include another conversation."),
  # T2-048
  dict(name="nonromantic life partner", kind="partner", ways="W U",
       profiles=[("W U", "Builds a deliberate shared life through clear, mutually chosen responsibilities."),
                 ("G", "Experiences a lasting bond as the form of belonging that fits their lives."),
                 ("B", "Chooses a shared life on their own terms rather than the form others expect.")],   # third: Library
       meets="need:belonging+.08 need:safety+.05 need:autonomy-.05 res:money+.03",
       ages=(20, 110), share=.01,   # estimate
       say="in a nonromantic life partnership",
       gained="two close friends, often after years of sharing a flat or seeing each other through 'a long dark "
              "season', agree to build their lives together without romance",
       lost="ending or reshaping the partnership, 'falling in love' with someone else, a death",
       needs="two adults who both agree; age 20 or more; not a marriage, a tenancy or legal next of kin unless they "
             "arrange one",
       turning="A form offers only spouse, relative or friend. None quite describes the responsibilities they have "
               "chosen."),
  # T2-049
  dict(name="spouse in a family-arranged marriage", kind="partner", ways="G W", refines="wife or husband; married again",
       profiles=[("G W", "Finds a chosen partnership within an existing web of family relationships."),
                 ("B", "Negotiates the introduction and marriage as a deliberate personal decision.")],
       meets="need:belonging+.03 need:autonomy-.02 res:ties+.03",
       ages=(18, 110), share=.02,   # estimate: common in some communities, rare in most of the population
       say="married through a family introduction",
       gained="a family introduction, meetings with both families and then alone, and a marriage both adults freely "
              "choose: 'getting married'",
       lost="the marriage settling into another description such as [partner of many years], a separation, "
            "'your partner dies'",
       needs="[wife or husband]; a consensual adult marriage: an arranged introduction is not a forced marriage"),
  # T2-050
  dict(name="partner in a multigenerational household", kind="partner", ways="G B", refines="wife or husband; living together; married again; partner of many years",
       profiles=[("G B", "Combines household continuity with negotiated space for the couple's own life."),
                 ("U R", "Learns and experiments with ways of sharing a home across generations.")],
       meets="need:autonomy-.05 res:ties+.05 res:money+.03 res:time-.03",
       ages=(18, 110), share=.06,   # about 18% of Americans lived in a multigenerational home in 2021 (Pew), fewer in
                                    # most of Europe; estimate for a couple sharing a home with a parent
       say="in a multigenerational household",
       gained="'a parent comes to stay for a week' and stays, or the couple moves in with parents to share the rent "
              "and the care",
       lost="moving to a home of their own, a separation, the household changing when the older generation dies or "
            "moves into care",
       needs="[wife or husband] and a living parent under the same roof; who owns or rents the home is recorded "
             "separately"),

  # ---------- children: facets on [mother or father] and [grandparent], and one guardianship of its own kind
  # T2-051
  dict(name="parent of an only child", kind="children", ways="G U", refines="mother or father",
       profiles=[("G U", "Learns the particular child's needs without assuming one family pattern suits everyone."),
                 ("R", "Makes room for a close, expressive relationship and the child's growing individuality.")],
       meets="",   # Emren: it inherits the parenthood effects of [mother or father]
       ages=(16, 110), share=.15,   # about 1 US mother in 5 at the end of her childbearing years has one child (Pew
                                    # 2015); estimate
       say="the parent of an only child",
       gained="a few years after 'a child is born' with no brother or sister following, the one-child family becomes "
              "the way the household is described",
       lost="another child joining the family; parenthood itself remains",
       needs="[mother or father] with one child; no prediction about children to come"),
  # T2-052
  dict(name="parent of independent adult children", kind="children", ways="G", refines="mother or father",
       profiles=[("G", "Accepts that care continues while daily control and responsibility recede."),
                 ("U", "Learns a new relationship based on adult-to-adult communication."),
                 ("B R", "Reclaims the freedom and ambitions that years of daily parenting set aside.")],   # third: Library
       meets="need:autonomy+.05 res:time+.08",   # gives back part of the time [mother or father] still charges
       ages=(36, 110), share=.55,   # estimate: most parents see the youngest settled on their own
       say="the parent of grown-up children",
       gained="'the children leave home': the youngest settles on their own, and parenting becomes adult to adult",
       lost="a return to intensive care, another phase of parenting such as [grandparent]; the family history remains",
       needs="[mother or father] with no child at home who needs daily care",
       turning="The old advice is ready on the tongue. This time, the parent asks whether advice is wanted."),
  # T2-053
  dict(name="parent with a child living abroad", kind="children", ways="R G", refines="mother or father",
       profiles=[("R G", "Keeps affection and family roots alive across distance."),
                 ("W U", "Builds dependable arrangements for contact and practical responsibilities.")],
       meets="res:ties-.03 res:money-.03",
       ages=(36, 110), share=.08,   # estimate: emigrants are a few in 100 of the native-born in most rich countries
                                    # (OECD), and a parent of two or three has two or three chances
       say="a parent with a child abroad",
       gained="a grown child takes a job, a degree or a partner in another country; 'a long-planned trip' becomes a "
              "visit",
       lost="the child coming back, the parent moving to join them, a different care arrangement",
       needs="[mother or father] and a grown child living in another country"),
  # T2-054
  dict(name="home-educating parent", kind="children", ways="U R", refines="mother or father",
       profiles=[("U R", "Adapts learning through curiosity, experimentation and the child's interests."),
                 ("W", "Accepts a sustained educational responsibility and works to provide a dependable structure."),
                 ("B", "Takes charge of the child's education to pursue the opportunities the family judges best.")],
                 # third: Library
       meets="need:meaning+.05 need:belonging+.03 res:time-.12 res:money-.05", lasts=12,
       ages=(20, 70), share=.03,   # US: about 3 school-age children in 100 were home-schooled in 2019 (NCES), more
                                   # since 2020; about 1 in 100 in England; estimate
       say="a home-educating parent",
       gained="the household registers a home-education arrangement where the law allows it, after an unhappy spell "
              "at school, a move or a long-held wish, and the child has a say",
       lost="a return to school or college, the end of compulsory schooling, the responsibility passing to someone else",
       needs="[mother or father] with a child of school age at home; local eligibility and a real educational "
             "responsibility"),
  # T2-055
  dict(name="guardian of an unrelated child", kind="children", ways="W B",
       profiles=[("W B", "Accepts explicit responsibility while protecting the child's practical interests and "
                         "agency."),
                 ("G", "Builds continuity and belonging in a relationship not based on shared ancestry.")],
       meets="need:meaning+.1 need:autonomy-.03 res:time-.12 res:money-.05",
       ages=(21, 85), share=.003,   # estimate: far rarer than fostering or adoption
       say="a child's guardian",
       gained="named guardian in the will of a close friend, or appointed by a court under the rules of the setting; "
              "'you take in a child who needs a home'",
       lost="the guardianship ending, an adoption, another arrangement, the child growing up and setting out alone",
       needs="a recognised guardianship of a child who is not a relative; age 21 or more; distinct from [foster "
             "parent], [adoptive parent] and babysitting"),
  # T2-056
  dict(name="grandparent raising a grandchild", kind="children", ways="G W", refines="grandparent",
       profiles=[("G W", "Carries family continuity into a new period of daily care."),
                 ("B", "Uses experience and resources to protect the grandchild's future options.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.12 res:money-.05 res:health-.03", lasts=18,
       ages=(38, 90), share=.02,   # US: over 2 million grandparents are responsible for grandchildren living with
                                   # them (Census ACS); estimate
       say="raising a grandchild",
       gained="a grandchild comes to live with them for the long term, by a family arrangement or a kinship order; "
              "'you take in a child who needs a home'",
       lost="care passing back to a parent or to someone else, the grandchild growing up and leaving, another family "
            "arrangement",
       needs="[grandparent] and the daily care of the grandchild; legal authority is recorded separately",
       turning="The school gate is familiar, but the other parents belong to their children's generation."),
  # T2-057
  dict(name="parent coordinating complex support needs", kind="children", ways="W U", refines="mother or father",
       profiles=[("W U", "Coordinates services and routines so a child's actual needs are met."),
                 ("B R", "Advocates firmly and creatively when standard arrangements fail the child.")],
       meets="need:meaning+.05 need:autonomy-.03 res:time-.1 res:money-.05",
       ages=(16, 100), share=.05,   # England: about 5 pupils in 100 have an education, health and care plan (DfE
                                    # 2024); estimate
       say="coordinating a child's support",
       gained=("an assessment or a diagnosis is followed by years of plans, appointments and meetings with the school "
               "and other services, where [handling red tape] is learned the hard way"),
       lost="the needs changing, the coordination passing to someone else, an adult child taking charge with the "
            "right support",
       needs="[mother or father] and substantial real coordination work; the condition of the child carries no color"),
  # T2-058
  dict(name="parent raising a child across languages", kind="children", ways="G R", refines="mother or father",
       profiles=[("G R", "Makes multiple languages part of family belonging and everyday expression."),
                 ("U", "Learns how to support the child's changing use and understanding of languages."),
                 ("B", "Treats each language as an advantage the child will carry into later life.")],   # third: Library
       meets="need:meaning+.03 res:ties+.03 res:time-.03",
       ages=(16, 80), share=.1,   # US: about 1 child in 5 speaks a language other than English at home (Census
                                  # ACS); estimate for an active practice
       say="raising a child in more than one language",
       gained="a household keeps two or more languages alive in bedtime stories, calls with the grandparents and "
              "weekend classes; [second language] or [family abroad] helps",
       lost="the practice fading, the child growing up and leaving home, another description of the parenting "
            "coming to matter more",
       needs="[mother or father] with a child at home and an active practice, not only parents of different "
             "nationalities"),

  # ---------- community: up to three at once ([club member] stays the generic adult club)
  # T2-059
  dict(name="choir member", kind="community", sphere="arts", face="arts.W", ways="W G",
       profiles=[("W G", "Sustains a shared musical practice through belonging and preparation."),
                 ("B", "Develops a chosen public voice and a place beyond their usual social role.")],
       meets="need:belonging+.08 need:meaning+.03 res:time-.05",
       ages=(8, 100), share=.12,   # UK: about 2.1 million people sing in some 40,000 choirs (Voices Now 2017);
                                   # estimate for ever, school choirs included
       say="in a choir",
       gained="an audition or an open rehearsal on a weeknight leads to regular membership: a school, church or "
              "community choir",
       lost="leaving, a move ('moved away'), the choir closing",
       needs="a willing ensemble and whatever audition in [singing] it asks",
       turning="The newest member has a beautiful voice but keeps rushing the shared phrase. The choir has to make "
               "room without losing each other."),
  # T2-060
  dict(name="community-garden coordinator", kind="community", ways="G U",
       profiles=[("G U", "Learns what the place and its growers need over time."),
                 ("W B", "Negotiates plots and responsibilities so a shared resource remains workable.")],
       meets="need:meaning+.05 need:belonging+.05 res:time-.08",
       ages=(18, 90), share=.01,   # estimate
       say="the community garden's coordinator",
       gained="the garden members ask them to coordinate the next season, often after years of 'tending an allotment'",
       lost="handing over at the yearly meeting, a move, the landowner withdrawing permission for the site",
       needs="a mandate from the members and access to the garden; [growing food] helps"),
  # T2-061
  dict(name="repair-cafe volunteer", kind="community", sphere="learn", face="learn.R", ways="U W",
       profiles=[("U W", "Makes practical knowledge useful to others through reliable help."),
                 ("R G", "Enjoys the encounter with a stubborn object and the person who brought it.")],
       meets="need:meaning+.05 res:ties+.05 res:time-.05",
       ages=(16, 90), share=.005,   # estimate: some thousands of repair cafes worldwide, most in the Netherlands,
                                    # Germany, Belgium and Britain
       say="a repair-cafe volunteer",
       gained="a monthly repair event in the library or a church hall becomes a regular commitment",
       lost="stepping back, the venue closing, a move",
       needs="[fixing things], [sewing and mending] or another repair skill, and the agreed limits of the group"),
  # T2-062
  dict(name="amateur astronomer in a club", kind="community", sphere="learn", face="learn.U", ways="U",
       profiles=[("U", "Shares careful observation and persistent questions."),
                 ("R G", "Joins because looking at the night sky feels astonishing and grounding.")],
       meets="need:meaning+.05 need:belonging+.03 need:competence+.03 res:time-.05 res:money-.02",
       ages=(10, 100), share=.005,   # estimate
       say="an amateur astronomer",
       gained="a public observing evening, 'more stars than anyone could count' or 'the sun goes dark at noon' leads "
              "to joining a club",
       lost="leaving, a move, the club winding down",
       needs="membership and access to observing sessions; a [good telescope] helps but is not required"),
  # T2-063
  dict(name="historical reenactment member", kind="community", sphere="arts", face="arts.G", ways="G W",
       profiles=[("G W", "Keeps a shared practice alive through craft and group responsibilities."),
                 ("B R", "Uses performance to try an expressive identity far from everyday work.")],
       meets="need:belonging+.08 need:autonomy+.03 res:money-.03 res:time-.05",
       ages=(14, 85), share=.004,   # estimate
       say="a historical reenactor",
       gained="a public event at a castle or an old battlefield leads to joining a group, its drill and its sewing "
              "evenings",
       lost="leaving, interests changing, the group closing",
       needs="a place in the group, [period kit] and the safety arrangements its events require",
       turning="Someone asks whether the costume is accurate. Someone else asks whose history never gets "
               "represented."),
  # T2-064
  dict(name="community-radio presenter", kind="community", ways="R U",
       profiles=[("R U", "Explores ideas and voices through an expressive format."),
                 ("W", "Provides dependable local information that larger broadcasters overlook."),
                 ("B", "Builds a voice and a following of their own outside the larger stations.")],   # third: Library
       meets="need:meaning+.05 need:competence+.03 res:ties+.03 res:time-.05",
       ages=(16, 90), share=.004,   # estimate; a paid presenter holds a career instead
       say="a community-radio presenter",
       gained="a trial programme on the local station becomes a regular weekly slot",
       lost="the slot ending, the station closing, stepping back",
       needs="the approval of the station and its production training; [public speaking] helps",
       turning="A neighbour with no broadcasting experience tells a story nobody else in town has covered."),
  # T2-065
  dict(name="community-mediation volunteer", kind="community", sphere="rule", face="rule.G", ways="W U",
       profiles=[("W U", "Helps people understand a dispute and find an accountable process."),
                 ("G", "Protects the possibility of living alongside each other after the dispute.")],
       meets="need:meaning+.05 need:competence+.03 res:time-.05 res:health-.02",
       ages=(21, 85), share=.004,   # estimate
       say="a volunteer mediator",
       gained="a training course in [settling disputes] leads to supervised mediation of disputes between neighbours",
       lost="leaving the service, no longer meeting its suitability rules, the service closing",
       needs=("mediation training ([mediation accreditation]), impartiality and a recognised service; [calming people "
              "down]")),
  # T2-066
  dict(name="search-and-rescue volunteer", kind="community", sphere="care", face="care.R", ways="W R",
       profiles=[("W R", "Accepts preparation and teamwork for moments requiring decisive help."),
                 ("U", "Finds commitment in mastering a demanding coordinated practice."),
                 ("B G", "Tests their own endurance against terrain and weather they know closely.")],   # third: Library
       meets="need:meaning+.08 need:belonging+.05 res:time-.08 res:health-.02",
       ages=(18, 70), share=.003,   # estimate
       say="a search-and-rescue volunteer",
       gained="selection, a probationary year and training lead to a place in a recognised mountain, cave or lowland "
              "rescue team",
       lost="stepping back, a move, no longer meeting the fitness and readiness rules",
       needs=("team-specific skills ([navigation], [emergency care]) and authorisation; [first-aid certificate]; good "
              "health")),
  # T2-067
  dict(name="lifeboat volunteer", kind="community", sphere="care", face="care.R", ways="W G",
       profiles=[("W G", "Protects a coastal community through dependable service."),
                 ("B R", "Chooses a demanding practical commitment that gives life personal direction.")],
       meets="need:meaning+.08 need:belonging+.05 need:safety-.02 res:time-.08",
       ages=(17, 65), share=.002,   # estimate: the British and Irish lifeboat service has about 5,000 volunteer crew
                                    # (RNLI); a lifeboat station is needed
       say="lifeboat crew",
       gained="a coastal rescue station recruits and trains them; the pager goes on the first night",
       lost="leaving, moving inland, losing operational eligibility through age or health",
       needs=("selection, sea training ([boat handling], [sea survival certificate]) and operational authorisation; "
              "[swimming]; living near the station")),
  # T2-068
  dict(name="school-governance board member", kind="community", sphere="learn", face="learn.W", ways="W U",
       profiles=[("W U", "Reviews decisions and responsibilities affecting a school community."),
                 ("B G", "Protects a school's local continuity while negotiating resources.")],
       meets="need:meaning+.05 res:ties+.03 res:time-.05",
       ages=(18, 85), share=.02,   # England has about 250,000 school governors and trustees (National Governance
                                   # Association); estimate for ever
       say="a school governor",
       gained="a parent election or a community appointment brings a seat on the board of a school",
       lost="the term ending, resigning, removal",
       needs=("eligibility, with [cleared to work with children], and formal appointment; often a child at the school "
              "or [good name in town]")),
  # T2-069
  dict(name="parent-association organiser", kind="community", ways="R W",
       profiles=[("R W", "Turns concern for children into shared practical action."),
                 ("U B", "Makes the association effective by understanding constraints and building leverage.")],
       meets="need:belonging+.05 need:meaning+.05 res:time-.05",
       ages=(18, 70), share=.04,   # estimate
       say="running the parents' association",
       gained="other parents at the school gate ask them to organise the year: the summer fair, the quiz night, the "
              "coat drive",
       lost="handing over, the children changing schools or growing up, the group ending",
       needs="a child at the school and a recognised role in the group; not a governance mandate"),
  # T2-070
  dict(name="housing-cooperative member", kind="community", sphere="comm", face="comm.G", ways="G W",
       profiles=[("G W", "Shares responsibility for a place to live over the long term."),
                 ("U B", "Uses collective ownership or governance to gain practical control through informed "
                         "decisions.")],
       meets="need:belonging+.05 need:autonomy+.03 res:money-.03 res:time-.03",
       ages=(18, 110), share=.04,   # estimate: cooperative housing is common in Scandinavia and parts of Germany and
                                    # Switzerland, rare in Britain and the US
       say="a member of a housing cooperative",
       gained="they buy a share or come up the waiting list, move in, and take on the duties of membership: meetings, "
              "a rota, a vote on the budget",
       lost="selling or giving up the membership, a move, the cooperative dissolving",
       needs="actual membership and whatever housing and financial conditions the cooperative sets",
       turning="The roof needs money now; three households cannot afford the proposed contribution."),
  # T2-071
  dict(name="sports referee", kind="community", sphere="gather", face="gather.W", ways="W",
       profiles=[("W", "Keeps a contest workable through consistent judgment."),
                 ("R", "Loves the live pace and the challenge of responding clearly in the moment.")],
       meets="need:competence+.05 need:belonging-.02 res:ties+.03 res:time-.05",
       ages=(14, 75), share=.02,   # estimate: most who earn the referee's badge officiate for a while; a paid
                                   # referee holds a career instead
       say="a referee",
       gained="the course for [referee's badge], then regular appointments to youth and amateur fixtures",
       lost="stopping appointments, the badge lapsing, interests changing; the knees go",
       needs="[referee's badge] and the approval of the competition"),
  # T2-072
  dict(name="festival organiser", kind="community", sphere="gather", face="gather.G", ways="R U",
       profiles=[("R U", "Invents an occasion that brings different experiences together."),
                 ("W B", "Makes a public celebration feasible through agreements, budgets and clear "
                         "responsibilities.")],
       meets="need:meaning+.05 need:belonging+.05 res:time-.08",
       ages=(16, 85), share=.01,   # estimate
       say="a festival organiser",
       gained="the planning group behind 'a festival comes to town' or the yearly street party gives them an ongoing "
              "organising role",
       lost="handing over, cancellation, 'burnout'",
       needs="an actual mandate and the event permissions the council requires"),
  # T2-073
  dict(name="amateur band member", kind="community", sphere="arts", face="arts.R", ways="R",
       profiles=[("R", "Shares direct expression and the pleasure of making music together."),
                 ("U", "Builds music through arrangements, constraints and systematic rehearsal.")],
       meets="need:belonging+.05 need:autonomy+.05 res:time-.05 res:money-.02",
       ages=(12, 90), share=.08,   # estimate
       say="in a band",
       gained="'a band or a sport that takes over your life': a rehearsal in a garage becomes a continuing place in "
              "the band",
       lost="leaving, the band splitting, a move",
       needs="[musical instrument] or [singing], and a willing group"),
  # T2-074
  dict(name="book-club organiser", kind="community", sphere="gather", face="gather.U", ways="U G",
       profiles=[("U G", "Helps people understand books in the context of their lives."),
                 ("B", "Creates a space for independent judgment beyond established cultural gatekeepers."),
                 ("R", "Picks books that spark strong feelings and lively argument.")],   # third: Library
       meets="need:meaning+.05 res:ties+.05 res:time-.03",
       ages=(16, 95), share=.02,   # estimate
       say="the book club's organiser",
       gained="they start arranging the monthly meetings and choosing the books, in a front room, a library or a cafe",
       lost="handing over, the group ending, a move",
       needs="willing readers and a recurring organising role"),
  # T2-075
  dict(name="community-kitchen volunteer", kind="community", sphere="gather", face="gather.W", ways="W G",
       profiles=[("W G", "Makes nourishment a reliable shared practice."),
                 ("B R", "Builds a practical space where people can contribute and eat on their own terms.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05 res:health-.02",
       ages=(16, 90), share=.03,   # estimate
       say="a community-kitchen volunteer",
       gained="a meal service or a food bank takes them onto its weekly rota, often after 'a volunteer drive in your "
              "neighbourhood'",
       lost="stepping back, the service closing, another commitment taking priority",
       needs="an induction, food-safety training ([food hygiene certificate]) and agreed duties"),
  # T2-076
  dict(name="neighbourhood-watch coordinator", kind="community", sphere="prot", face="prot.G", ways="W U",
       profiles=[("W U", "Organises clear, proportionate information-sharing and reporting."),
                 ("G", "Cares about familiar neighbours and everyday continuity.")],
       meets="need:safety+.03 res:ties+.03 res:time-.03",
       ages=(21, 90), share=.015,   # estimate
       say="the neighbourhood-watch coordinator",
       gained="after 'break-ins on the street', residents ask them to coordinate an agreed local scheme",
       lost="handing over, a move, the scheme ending",
       needs="a recognised community role with clear limits; no police authority"),
  # T2-077
  dict(name="prison visitor", kind="community", ways="G W",
       profiles=[("G W", "Maintains human connection across a setting that separates people from ordinary life."),
                 ("B", "Supports a person's continuing agency and identity beyond their conviction.")],
       meets="need:meaning+.08 res:ties+.02 res:time-.03",
       ages=(21, 85), share=.002,   # estimate
       say="a prison visitor",
       gained="a recognised visiting scheme accepts them after checks and training",
       lost="the arrangement ending, withdrawing, a move",
       needs="the approval of the prison, training and the agreement of the person visited",
       turning="A conversation about an ordinary television programme matters because almost every other "
               "conversation has been about the person's case."),
  # T2-078
  dict(name="board-game club organiser", kind="community", sphere="gather", face="gather.U", ways="U R",
       profiles=[("U R", "Designs a varied shared experience through rules, discovery and play."),
                 ("W", "Makes the club dependable and welcoming through fair practical arrangements.")],
       meets="need:belonging+.05 need:meaning+.03 res:time-.05 res:money-.02",
       ages=(14, 90), share=.01,   # estimate
       say="running a board-game club",
       gained="a recurring game night in a cafe or the back room of a pub grows into an organised club",
       lost="handing over, the venue closing, the club dispersing",
       needs="willing players, a venue or an online space, and a continuing role",
       turning="An experienced player wants a demanding game; the newcomer has never touched a rulebook. The evening "
               "needs a place for both."),

  # ---------- faith and causes: one at a time; paid ministry stays here
  # T2-079
  dict(name="ordained religious minister", kind="faith", sphere="faith", face="faith.W", ways="W G",
       profiles=[("W G", "Sustains shared ritual and care within a continuing tradition."),
                 ("U", "Treats interpretation and difficult questions as a lifelong responsibility."),
                 ("R", "Leads worship and pastoral care through felt conviction and personal presence.")],
                 # third: Library
       meets="need:meaning+.12 need:belonging+.05 need:autonomy-.05 res:ties+.05 res:time-.1 res:money+.08",
       ages=(23, 85), share=.004,   # estimate: clergy are a few workers in 1,000
       say="a minister of religion",
       gained=("years of training ([leading a ceremony]) and the community's own process of discernment lead to "
               "ordination and a recognised ministry"),
       lost="retirement, leaving ministry, the tradition withdrawing its recognition",
       needs="[regular worshipper] or [convert] for years; [scripture]; the recognition and requirements of the "
             "tradition, often with [graduate]"),
  # T2-080
  dict(name="member of a monastic community", kind="faith", sphere="faith", face="faith.U", ways="W G",
       profiles=[("W G", "Orders daily life around shared spiritual practice and continuity."),
                 ("B", "Freely chooses a demanding life that rejects a socially expected route to status or "
                       "consumption.")],
       meets="need:meaning+.12 need:belonging+.1 need:autonomy-.1 res:time-.1 res:freedom-.05",
       ages=(18, 110), share=.001,   # estimate
       say="a member of a monastic community",
       gained="a period of discernment, stays as a guest, then years as a novice before accepted membership",
       lost="leaving, moving to another community, death",
       needs="voluntary adult participation and the admission process of the community; usually no partner and no "
             "children at home",
       turning="The quiet life still contains washing up, disagreement and a person whose habits are difficult to "
               "bear."),
  # T2-081
  dict(name="lay religious teacher", kind="faith", sphere="faith", face="faith.U", ways="W U",
       profiles=[("W U", "Helps others understand a tradition with care and consistency."),
                 ("R", "Teaches through stories, feeling and vivid connection to ordinary life."),
                 ("G", "Passes the tradition on as it was handed down, within the shared life of the community.")],
                 # third: Library
       meets="need:meaning+.08 need:competence+.05 res:ties+.03 res:time-.05",
       ages=(16, 90), share=.03,   # estimate
       say="a lay teacher of the faith",
       gained="the congregation asks them to lead a recurring class: Sunday school, a study group, weekend lessons "
              "for the children",
       lost="stepping down, a change in faith, the class ending",
       needs="[regular worshipper] for some years; [scripture] or [teaching]; recognition by the community; distinct "
             "from [teacher]"),
  # T2-082
  dict(name="congregation musician", kind="faith", sphere="faith", face="faith.R", ways="R W",
       profiles=[("R W", "Gives shared belief an expressive public form."),
                 ("U", "Develops the musical structure and technique that let others participate.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05",
       ages=(12, 90), share=.02,   # estimate
       say="the congregation's musician",
       gained="a regular place at the organ, in the band or leading the singing replaces occasional help",
       lost="stepping back, a move to another congregation, leaving the role",
       needs="[musical instrument] or a trained voice ([singing]), and the agreement of the congregation",
       turning="A familiar song no longer fits the occasion. Changing it may feel like care to some and loss to "
               "others."),
  # T2-083
  dict(name="interfaith-dialogue participant", kind="faith", sphere="faith", face="faith.U", ways="W U",
       profiles=[("W U", "Builds careful understanding across differences without demanding agreement."),
                 ("R G", "Values the lived encounter, hospitality and unfamiliar practices of other communities.")],
       meets="need:meaning+.05 need:safety-.02 res:ties+.05 res:time-.03",
       ages=(16, 95), share=.01,   # estimate
       say="in an interfaith dialogue circle",
       gained="a dialogue circle between local congregations, begun with a shared meal or a vigil, becomes a "
              "continuing commitment",
       lost="leaving, the circle ending, another commitment",
       needs="a faith held for some years, voluntary participation and a recurring group"),
  # T2-084
  dict(name="animal-shelter campaigner", kind="faith", ways="G W",
       profiles=[("G W", "Works for durable responsibility toward animals in human care."),
                 ("B R", "Turns fierce personal concern into independent organising and fundraising.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.05 res:money-.02",
       ages=(14, 95), share=.02,   # estimate
       say="an animal-shelter campaigner",
       gained="repeated help at the shelter after 'a stray dog follows you home' or 'a pet of your own' grows into "
              "fundraising and campaigning",
       lost="the campaign ending, stepping back, a change of cause",
       needs="a real campaign role; handling the animals needs its own training ([handling animals])"),
  # T2-085
  dict(name="disability-rights organiser", kind="faith", ways="W B",
       profiles=[("W B", "Combines collective rights with individual control over one's life."),
                 ("U R", "Develops new forms of access and challenges assumptions through creative campaigning.")],
       meets="need:meaning+.08 need:autonomy+.03 res:time-.05 res:health-.02",
       ages=(16, 95), share=.01,   # estimate
       say="a disability-rights organiser",
       gained=("a local barrier, a step with no ramp or a form nobody can use, leads to continuing organising and "
               "[campaigning] with the people it affects"),
       lost="handing over, leaving the group, other commitments",
       needs="a recognised role in the cause and accountable participation; no disability status is required"),
  # T2-086
  dict(name="civil-liberties campaigner", kind="faith", ways="W B",
       profiles=[("W B", "Defends rights that protect people from arbitrary interference."),
                 ("R", "Acts because suppressed expression or constrained freedom feels intolerable.")],
       meets="need:meaning+.08 need:safety-.03 res:ties+.03 res:time-.05",
       ages=(16, 95), share=.01,   # estimate
       say="a civil-liberties campaigner",
       gained="'a sense of injustice' over one case, a protest or 'a bitter election' becomes a sustained campaign",
       lost="a campaign ending, 'burnout', a change of cause",
       needs="an actual group or an ongoing independent campaign",
       turning="The person whose right they are defending holds views they strongly dislike."),
  # T2-087
  dict(name="restorative-justice advocate", kind="faith", ways="G U",
       profiles=[("G U", "Seeks ways for repair to fit the actual people and context."),
                 ("R W", "Combines emotional recognition with obligations that make repair credible.")],
       meets="need:meaning+.08 need:belonging+.03 res:ties-.02 res:time-.05",
       ages=(18, 95), share=.005,   # estimate
       say="a restorative-justice advocate",
       gained="study, a court case close to home or being 'robbed or attacked in the street' leads to a sustained "
              "advocacy role",
       lost="leaving the cause, handing over, a change of approach",
       needs=("a cause commitment; facilitating a formal meeting needs separate training in [settling disputes] "
              "([mediation accreditation]) and the consent of everyone involved")),
  # T2-088
  dict(name="digital-rights advocate", kind="faith", ways="U B",
       profiles=[("U B", "Understands systems to protect practical agency and control over personal information."),
                 ("W G", "Defends the continuity of shared digital resources people depend on.")],
       meets="need:meaning+.05 need:competence+.05 res:time-.05",
       ages=(16, 95), share=.005,   # estimate
       say="a digital-rights advocate",
       gained="a technology decision, a new surveillance scheme or a data leak, leads to sustained public-interest "
              "work",
       lost="stepping back, a change of cause, the group closing",
       needs="an ongoing cause role; [writing code] helps, but technical authority is not automatic",
       turning="The convenient new platform would make a volunteer group's work easier, but nobody knows who can keep "
               "its records."),

  # ---------- status: no colors, no destiny; any number at once
  # T2-089
  dict(name="doctoral graduate", kind="status", ways="",
       meets="need:competence+.03", lasts="life",   # only what it adds: [graduate] stays beside it with its own bonus
       ages=(24, 110), share=.01,   # about 1 adult in 100 aged 25 to 64 holds a doctorate across the OECD (OECD,
                                    # Education at a Glance)
       say="a doctoral graduate",
       gained="three to six years of research after a first degree, an examined thesis, then 'earning a qualification'",
       lost="never; a legal invalidation would be its own event",
       needs="[graduate]; the actual award of the doctorate, not only the study"),
  # T2-090
  dict(name="first-generation university student", kind="status", ways="",
       meets="need:meaning+.03 need:competence-.02", lasts=6,   # only while studying; 6 caps it
       ages=(17, 30), share=.15,   # US: 56% of undergraduates in 2015-16 had no parent with a bachelor's degree (RTI
                                   # for NASPA); estimate for ever
       say="the first in the family at university",
       gained="enrolment at a university when neither parent holds a degree; 'you win a scholarship or a place'",
       lost="graduating ([graduate]) or leaving the course; the history remains",
       needs="actual enrolment and a [school-leaving certificate]; first generation here means no parent with a "
             "university degree"),
  # T2-091
  dict(name="former foster child", kind="status", ways="",
       meets="", lasts="life",
       ages=(1, 110), share=.03,   # US: about 6 children in 100 are placed in foster care before 18 (Wildeman and
                                   # Emanuel 2014); fewer in most of Europe; estimate
       say="a former foster child",
       gained="'going into foster care' in childhood, which ends with a return home, an adoption, a guardianship or "
              "leaving care as a young adult",
       lost="never; it is a fact of their history",
       needs="a recorded foster placement in childhood"),
  # T2-092
  dict(name="adopted person", kind="status", ways="",
       meets="", lasts="life",
       ages=(0, 110), share=.02,   # about 2 children in 100 in the US are adopted (US Census 2010)
       say="adopted",
       gained="an adoption in childhood, by new parents, a stepparent or relatives, as the law of the setting defines it",
       lost="never; it is a fact of their history",
       needs="a recorded adoption; distinct from being an [adoptive parent]"),
  # T2-093
  dict(name="refugee", kind="status", ways="",
       meets="", lasts="life",
       ages=(0, 110), share=.01,   # estimate: refugees are a few residents in 100 in Germany and Sweden, far fewer in
                                   # most rich countries (UNHCR)
       say="a refugee",
       gained="protection granted on a claim for asylum ([asylum applicant]), or resettlement through a refugee "
              "programme",
       lost="the legal status changing, usually with [citizenship]; the history of displacement remains",
       needs="an actual status decision; [immigrant] comes with it"),
  # T2-094
  dict(name="asylum applicant", kind="status", ways="",
       meets="need:safety-.05 res:freedom-.03", lasts=5,   # only while the claim is pending; 5 caps it
       ages=(0, 110), share=.015,   # estimate
       say="seeking asylum",
       gained="arrival after 'war comes' or persecution at home ('moved away'), and a claim for protection lodged with "
              "the authorities",
       lost="a decision ([refugee] or a refusal), a withdrawal, another procedural outcome",
       needs="a lodged application still under consideration"),
  # T2-095
  dict(name="naturalised citizen", kind="status", ways="",
       meets="", lasts="life",   # legal access is applied once, by [citizenship]
       ages=(5, 110), share=.08,   # as [citizenship]: the two come together (next version: .06 to .08, change-later.md)
       say="a naturalised citizen",
       gained="years of residence, a test on the history and laws, and an oath at a ceremony; [citizenship] comes with "
              "it",
       lost="almost never; current citizenship is tracked by [citizenship]",
       needs="[immigrant] and a completed grant of [citizenship]"),
  # T2-096
  dict(name="bankruptcy or insolvency in their history", kind="status", ways="",
       meets="", lasts="life",
       ages=(18, 110), share=.06,   # England and Wales: about 1 adult in 400 becomes insolvent each year (Insolvency
                                    # Service, 2023); estimate for ever
       say="someone who has been through bankruptcy",
       gained="'financial ruin': a bankruptcy, a debt relief order or an insolvency arrangement completed through the "
              "courts or an official process",
       lost="never as history; the active restrictions end when the process discharges",
       needs="a recorded formal process; ordinary debt is not enough"),
  # T2-097
  dict(name="on probation or community supervision", kind="status", ways="",
       meets="res:freedom-.05 res:time-.03", lasts=3,   # only while the order runs; 3 caps it
       ages=(10, 110), share=.04,   # US: about 1 adult in 70 was on probation at the end of 2021 (BJS); fewer in
                                    # Europe; estimate for ever
       say="on probation",
       gained="a court order after a conviction ([someone with a record]) or release from prison on licence "
              "([ex-prisoner]): appointments, conditions, unpaid work",
       lost="completing the order, an amendment, revocation or another legal outcome",
       needs="an actual order with stated conditions"),
  # T2-098
  dict(name="living in residential care", kind="status", ways="",
       meets="need:safety+.05 res:money-.05", lasts="life",
       ages=(18, 110), share=.15,   # estimate: about 1 death in 5 in England and Wales takes place in a care home (ONS)
       say="living in a care home",
       gained="'moving to a smaller home or into care': a residential home, a nursing home or supported housing with "
              "care on site",
       lost="moving elsewhere, another support arrangement, death",
       needs="actual residence and a defined arrangement for support"),
  # T2-099
  dict(name="returned migrant", kind="status", ways="",
       meets="res:ties+.03 res:money-.02", lasts=3,   # the return phase; the migration history remains
       ages=(18, 110), share=.05,   # estimate
       say="back home after years abroad",
       gained="after years abroad ('moved away'), a move back ('came home') to a country once regarded as home; "
              "'roots call the one who moved away'",
       lost="the return settling into ordinary life; the migration history remains",
       needs="a real return after a substantial spell abroad"),
  # T2-100
  dict(name="displaced by a disaster", kind="status", ways="",
       meets="need:safety-.08 res:money-.05 res:ties-.03", lasts=5,   # until a stable arrangement; 5 caps it
       ages=(0, 110), share=.04,   # estimate: the US Census Household Pulse Survey counts a few million adults
                                   # displaced by disasters each year, most of them for under a month
       say="displaced by a disaster",
       gained="a flood, a fire, a storm or 'war comes' leaves the home unsafe or unusable: 'losing the home'",
       lost="a safe return, a settled new home, another stable arrangement; the event stays in their history",
       needs="a real displacement, not only living near 'a disaster in the next town'"),
]


# =============================== TITLES, volume 3: the "v22" update, A16 (Library, 2026-10-09) ===============================
# The titles held back in the release batch for want of a decided mechanic (change-later.md, "From the release batch"),
# taken in on Emren's "Implement A16" (10-08 23:44 UTC), and three more first jobs so the first career spreads over
# more entry titles (change-later.md; care worker is there already). Shares are estimates for the titles check (C-L4).
TITLES += [
  dict(name="warehouse worker", kind="career", sector="services", sphere="prod", face="prod.R", ways="B R",
       profiles=[("B R", "Works fast for the bonus and the overtime, and takes the shifts others turn down."),
                 ("W U", "Keeps the line moving: learns the scanner, the system and the safety rules, every shift.")],
       meets="res:money+.03 res:health-.03 res:time-.08 need:autonomy-.03",
       ages=(16, 70), share=.06,   # estimate: warehouse and storage workers are about 1 US worker in 80 (BLS), with
                                   # high turnover, so many more hold the job for a while, often as a first job
       say="a warehouse worker",
       gained="'your first real job' through an agency, 'a new job at last' on the night shift at a distribution centre",
       lost="the contract ending, an injury, a better job",
       needs="a safety induction; a forklift ticket helps"),
  dict(name="receptionist", kind="career", sector="services", ways="W U",
       profiles=[("W U", "Keeps the front desk in order and knows where everything and everyone is."),
                 ("G", "The warm first face people see, who remembers their names.")],
       meets="res:money+.02 need:belonging+.02 res:time-.08",
       ages=(16, 75), share=.05,   # estimate: receptionists are about 1 US worker in 150 (BLS), with high turnover
       say="a receptionist",
       gained="'a job interview' for the front desk of a clinic, an office or a hotel, often as 'your first full-time job'",
       lost="another job, the desk replaced by a screen, retirement",
       needs="a tidy manner and a little computer skill"),
  dict(name="security guard", kind="career", sector="services", sphere="prot", face="prot.W", ways="W",
       profiles=[("W", "Keeps order at the door and by the book."),
                 ("U", "Watches the screens through the night and notices what others miss.")],
       meets="res:money+.02 need:safety-.02 res:time-.1 res:health-.02",
       ages=(18, 75), share=.05,   # estimate: security guards are about 1 US worker in 150 (BLS), many of them for a
                                   # few years, often as a first or a second job
       say="a security guard",
       gained="'a new job at last' with a security firm, after a short licence course",
       lost="the contract moving to another firm, nights wearing them down, another job",
       needs="a clean record in most places, and the guard's licence"),
  dict(name="union member", kind="community", sphere="prod", face="prod.W", ways="W R",
       profiles=[("W R", "Keeps faith with the people they work beside, and stands with them when it counts."),
                 ("U B", "Knows the agreement line by line, and makes it pay for the members.")],
       meets="need:belonging+.03 need:safety+.02 res:money-.01",
       ages=(16, 90), share=.25,   # about 1 worker in 6 across the OECD belongs to a union (OECD 2019), more in the
                                   # public sector and in the past; estimate for ever holding a card
       say="a union member",
       gained="joining at work, or holding the line in 'a strike vote at work'",
       lost="leaving the job or the union, letting the card lapse",
       needs="a job with a union"),
  dict(name="street preacher", kind="faith", sphere="faith", face="faith.R", ways="W R",
       meets="need:meaning+.08 need:belonging-.02 res:time-.05",
       ages=(14, 100), share=.005,   # estimate: a few in a thousand ever preach in the open street
       say="a street preacher",
       gained="taking a box to the corner of the square in 'a revival fills the square'",
       lost="the fire going out, a congregation of their own, the police moving them on for good",
       needs="a faith held hard enough to say it out loud to strangers"),
  dict(name="conscientious objector", kind="status", ways="",
       meets="need:meaning+.03 need:belonging-.03", lasts="life",
       ages=(18, 110), share=.003,   # estimate: only where service is compulsory, and few of those called object
       say="a conscientious objector",
       gained="objecting on conscience before the board in 'the call to serve', and serving in a care home instead",
       lost="never; it stays on the record",
       needs="a call-up, and a board that accepts the objection"),
  dict(name="national service done", kind="status", ways="",
       meets="need:competence+.02 res:ties+.02", lasts="life",
       ages=(19, 110), share=.02,   # estimate: about 3 in 1,000 young adults a year are called in this setting, most
                                    # serve a term
       say="someone who did their national service",
       gained="the end of the term served after 'the call to serve'",
       lost="never",
       needs="[soldier] held through a term that began with 'the call to serve'"),
  dict(name="permanent resident", kind="status", ways="",
       meets="need:safety+.03", lasts="life",
       ages=(5, 110), share=.08,   # as [permanent residence], the perk that carries the access: the two come together
       say="a permanent resident",
       gained="'residence papers at the government office'",
       lost="[naturalised citizen] takes its place in how people name them; the perk stays",
       needs="[immigrant] or [refugee], years of legal residence"),
  dict(name="without papers", kind="status", ways="",
       meets="need:safety-.08 res:freedom-.08 res:money-.03", lasts=5,   # until papers come or they leave; 5 caps it
       ages=(5, 110), share=.01,   # estimate: undocumented people are a few residents in 100 in the US and fewer in
                                   # most of Europe
       say="living without papers",
       gained="a refused residence application in 'residence papers at the government office', and staying anyway",
       lost="papers granted at last, leaving the country, being sent back",
       needs="[immigrant] or [refugee]"),
  dict(name="served the old regime", kind="status", ways="",
       meets="need:safety-.03 need:belonging-.03", lasts="life",
       ages=(16, 110), share=.002,   # estimate: 'the old order falls' reaches about 2 lives in 100
       say="someone who served the old regime",
       gained="standing with the last of the old guard in 'the old order falls'",
       lost="never; the new order remembers",
       needs="the old order falling in their lifetime"),
  dict(name="veteran of a revolution", kind="status", ways="",
       meets="need:meaning+.03 need:belonging+.02", lasts="life",
       ages=(16, 110), share=.003,   # estimate: 'the old order falls' reaches about 2 lives in 100
       say="a veteran of the revolution",
       gained="pushing at the palace gates in 'the old order falls'",
       lost="never",
       needs="the old order falling in their lifetime"),
  dict(name="founder of a movement", kind="status", ways="",   # stage 3, C5 (stage3-rules.md section 5)
       meets="need:meaning+.05 need:autonomy+.03", lasts="life",
       ages=(25, 110), share=.001,   # estimate: 'a following of your own' reaches at most about 1 life in 1,000
       say="the founder of a movement",
       gained="founding a movement of their own in 'a following of your own'",
       lost="never",
       needs="a new movement founded in their lifetime, by them"),
  dict(name="known as a strike-breaker", kind="status", ways="",
       meets="need:belonging-.05 res:ties-.03", lasts=15,   # memories at work fade; 15 caps it
       ages=(18, 90), share=.02,   # estimate: about 3 lives in 10 meet a strike ballot, few keep working through it
       say="known as a strike-breaker",
       gained="voting no and working through the strike in 'a strike vote at work'",
       lost="a new workplace, the years",
       needs="a job with a union and a strike"),
]

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

# =============================== PERKS ===============================

# ---------- skill: what the hands, the body or the head can do; it fades by skill_half once unused
PERKS += [
  dict(name="swimming", kind="skill", ways="R G", odds=.04, skill_half=40, retires=None,
       ages=(4, 100), share=.8,   # estimate: about 1 adult in 5 in England says they cannot swim
       say="can swim",
       gained="lessons at the town pool, or a patient parent on 'a day at the beach'; "
              "'you never learned to swim' is the late chance",
       lost="only to an injury or great age",
       needs="'learned a skill'"),
  dict(name="cooking for a crowd", kind="skill", ways="G R W", odds=.04, skill_half=30, retires=None,
       ages=(10, 100), share=.35,   # estimate
       say="cooks for a crowd",
       gained="'learning to cook for yourself', a grandmother's kitchen, "
              "'a holiday meal with the whole family' at the stove",
       lost="only when the hands fail",
       needs="'learned a skill'"),
  dict(name="second language", kind="skill", ways="U R", odds=.06, skill_half=10, retires=None,
       ages=(3, 110), share=.45,   # about half of EU adults can hold a conversation in another language
                                   # (Eurobarometer 2012); fewer in the UK, far fewer in the US
       say="speaks a second language",
       gained="a parent's mother tongue, school lessons, 'a trip far from home', 'you take up an instrument or a language'",
       lost="years without speaking it",
       needs="'learned a skill' several times"),
  dict(name="musical instrument", kind="skill", ways="R U", odds=.04, skill_half=10, retires=None,
       ages=(5, 100), share=.25,   # estimate: many more start lessons than keep playing
       say="plays an instrument",
       gained="lessons as a child, 'you take up an instrument or a language', 'a band or a sport that takes over your life'",
       lost="putting it down for years",
       needs="'learned a skill' several times; an [instrument of one's own] to practise on"),
  dict(name="building trade", kind="skill", ways="U W", odds=.07, skill_half=15, retires=None,
       ages=(16, 80), share=.1,   # estimate: carpentry, plumbing, bricklaying and the like
       say="has a trade in their hands",
       gained="an apprenticeship and years on site; 'earning a qualification'",
       lost="a bad back ends the work, not the know-how",
       needs="[apprentice]; 'learned a skill' several times"),
  dict(name="fixing things", kind="skill", ways="U", odds=.03, skill_half=25, retires=None,
       ages=(10, 100), share=.45,   # estimate
       say="can fix things",
       gained="'the house needs repairs' and nobody to call; a parent's toolbox and a Saturday",
       lost="only when the hands fail",
       needs="'learned a skill'"),
  dict(name="car mechanics", kind="skill", ways="U R B", odds=.04, skill_half=12, retires=None,
       ages=(12, 90), share=.12,   # estimate
       say="knows engines",
       gained="a neighbour's shed, an old car that keeps breaking down, a garage job",
       lost="cars changing beyond recognition",
       needs="'learned a skill' several times"),
  dict(name="growing food", kind="skill", ways="G U", odds=.04, skill_half=30, retires=None,
       ages=(6, 100), share=.35,   # estimate
       say="grows food",
       gained="a grandmother's garden, 'tending an allotment', 'an afternoon in the garden'",
       lost="nothing; a flat with no garden suspends it",
       needs="a patch of earth and a season"),
  dict(name="sewing and mending", kind="skill", ways="G B", odds=.03, skill_half=30, retires=None,
       ages=(7, 100), share=.25,   # estimate
       say="can sew and mend",
       gained="taught at home or at school; 'a box of craft things and a free hour'",
       lost="eyes and fingers in old age",
       needs="'learned a skill'"),
  dict(name="public speaking", kind="skill", ways="W B", odds=.05, skill_half=8, retires=None,
       ages=(10, 100), share=.2,   # estimate
       say="can hold a room",
       gained="'a debate or contest at school', 'the school play', a best man's speech; "
              "'the club or congregation asks you to lead'",
       lost="years out of practice",
       needs="'learned a skill', and 'took a wild risk' the first time"),
  dict(name="bookkeeping", kind="skill", ways="W B", odds=.04, skill_half=10, retires=None,
       ages=(14, 100), share=.3,   # estimate
       say="keeps the books",
       gained="'a budget that will not balance' sorted at the kitchen table; "
              "'your first tax form and a stack of bills'; an evening class",
       lost="years of letting someone else do it",
       needs="'learned a skill'"),
  dict(name="boxing or martial arts", kind="skill", ways="R W", odds=.04, skill_half=8, retires=None,
       ages=(6, 75), share=.1,   # estimate
       say="can handle themselves",
       gained="a club in a church hall after 'a fight after school' or 'someone starts mocking you online'",
       lost="injury, age, stopping training",
       needs="'learned a skill' several times"),
  dict(name="dancing", kind="skill", ways="R G", odds=.03, skill_half=15, retires=None,
       ages=(4, 100), share=.3,   # estimate
       say="can dance",
       gained="'dancing at a wedding', Saturday classes, 'a festival weekend'",
       lost="the knees",
       needs="nerve"),
  dict(name="writing code", kind="skill", ways="U B", odds=.06, skill_half=5, retires=None,
       ages=(10, 90), share=.1,   # estimate
       say="writes code",
       gained="'a new hobby you cannot put down', a course, 'new technology changes your job'",
       lost="the tools moving on every five years",
       needs="'learned a skill' several times"),
  dict(name="drawing and painting", kind="skill", ways="R U", odds=.03, skill_half=15, retires=None,
       ages=(3, 110), share=.15,   # estimate
       say="can draw",
       gained="'a box of craft things and a free hour', 'the urge to make something', an art teacher who noticed",
       lost="years without a pencil",
       needs="'learned a skill'"),
  dict(name="home nursing", kind="skill", ways="G W", odds=.04, skill_half=20, retires=None,
       ages=(10, 100), share=.25,   # estimate
       say="knows how to nurse the sick",
       gained="being a [carer for a parent], a sick child, a friend down with 'flu, alone in a rented room'",
       lost="only forgetting",
       needs="'helped someone in need' several times"),
  dict(name="hunting and fishing", kind="skill", ways="G B", odds=.04, skill_half=20, retires=None,
       ages=(8, 90), share=.15,   # estimate
       say="can hunt and fish",
       gained="a grandparent's river at dawn, an uncle's rifle and a cold morning",
       lost="the eyes, the knees, or a move to the city",
       needs="patience; a [hunting licence] to hunt"),
  dict(name="selling", kind="skill", ways="B R", odds=.05, skill_half=10, retires=None,
       ages=(12, 90), share=.2,   # estimate
       say="can sell anything",
       gained="'a Saturday job at the corner shop', 'an idea for a side business', a year as a [salesperson]",
       lost="years away from it",
       needs="'made a friend' or 'took a wild risk'"),
  dict(name="finding things out", kind="skill", ways="U", odds=.05, skill_half=15, retires=None,
       ages=(8, 110), share=.3,   # estimate
       say="knows how to find things out",
       gained="'a curiosity that will not let go', a library card, a degree",
       lost="the mind slowing in great age",
       needs="'learned a skill'"),
  dict(name="minding small children", kind="skill", ways="W G", odds=.04, skill_half=20, retires=None,
       ages=(10, 100), share=.5,   # estimate
       say="is good with little ones",
       gained="'your little cousin comes to stay', babysitting, being a [mother or father]",
       lost="only the years",
       needs="'helped someone in need'"),
  dict(name="calming people down", kind="skill", ways="G U", odds=.05, skill_half=15, retires=None,
       ages=(12, 110), share=.2,   # estimate
       say="can calm people down",
       gained="night shifts as a [nurse], 'a teenager in your care breaks the rules', "
              "'you see a stranger being harassed' handled well",
       lost="years out of the thick of it",
       needs="'helped someone in need' several times"),
  dict(name="striking a deal", kind="skill", ways="B U", odds=.05, skill_half=10, retires=None,
       ages=(14, 100), share=.15,   # estimate
       say="drives a hard bargain",
       gained="'a bonus or a raise' asked for and won, a market stall, 'buying a home' at the right price",
       lost="years away from deals",
       needs="'took a wild risk'"),
  dict(name="scripture", kind="skill", ways="W G", odds=.03, skill_half=25, retires=None,
       ages=(6, 110), share=.15,   # estimate
       say="knows the scriptures",
       gained="years of Sunday school, madrasa or Hebrew school; being a [regular worshipper]",
       lost="only forgetting",
       needs="[regular worshipper] at some time"),
  dict(name="cards for money", kind="skill", ways="B R", odds=.03, skill_half=10, retires=None,
       ages=(14, 100), share=.1,   # estimate
       say="plays a sharp hand of cards",
       gained="a long winter of poker nights; 'a game of cards with old rivals'",
       lost="years away from the table",
       needs="'took a wild risk'"),
  dict(name="teaching", kind="skill", ways="W U R", odds=.04, skill_half=15, retires=None,
       ages=(14, 100), share=.3,   # estimate: training newcomers is part of many jobs and clubs (Library 2026-10-06, was .2)
       say="can explain anything",
       gained="'a younger colleague needs a mentor', being a [teacher] or a [youth coach]; 'years of practice are noticed'",
       lost="years of not doing it",
       needs="'learned a skill' and 'helped someone in need'"),
]

# ---------- credential: a licence, a certificate or a paper; it can be suspended or taken, and the skill under it stays
PERKS += [
  dict(name="driving licence", kind="credential", ways="R G", odds=0, skill_half=20, retires=None,
       ages=(17, 100), share=.85,   # about 3 adults in 4 in England hold a full licence (DfT); nearly 9 in 10 in
                                    # the US (FHWA)
       say="can drive",
       gained="lessons, a test failed once and passed the second time; 'a long car journey' as a passenger long before",
       lost="a ban for drink-driving, or 'the doctor says to stop driving'; the skill stays",
       needs="age 17 or 18; 'learned a skill'"),
  dict(name="first-aid certificate", kind="credential", ways="W R", odds=0, skill_half=3, retires=None,
       ages=(12, 100), share=.25,   # estimate
       say="knows first aid",
       gained="a day's course at work or with the scouts; it comes into its own when 'a stranger saves you, "
              "or you save one'",
       lost="it lapses after three years, and the know-how fades nearly as fast",
       needs="a day's course"),
  dict(name="passport", kind="credential", ways="R U", odds=0, skill_half=20, retires=None,
       ages=(0, 110), share=.75,   # estimate: most Britons and Europeans hold one; under half of Americans
                                   # (US State Department)
       say="has a passport",
       gained="'a trip far from home', 'a long-planned trip', a form and a photo booth",
       lost="it expires or is taken away; knowing how to travel stays",
       needs="citizenship somewhere, and the fee"),
  dict(name="school-leaving certificate", kind="credential", ways="W U", odds=0, skill_half=20, retires=None,
       ages=(16, 110), share=.85,   # about 8 adults in 10 have finished upper secondary school (OECD average)
       say="has finished school",
       gained="'exams are coming', and then they are passed",
       lost="never",
       needs="'learned a skill' several times"),
  dict(name="professional registration", kind="credential", ways="W U", odds=0, skill_half=10, retires=70,
       ages=(21, 75), share=.1,   # estimate: nurses, teachers, doctors, lawyers, engineers, social workers
       say="is registered to practise",
       gained="a degree, an exam and a yearly fee; 'earning a qualification'",
       lost="struck off after a complaint upheld, or let lapse; the knowledge stays",
       needs="[graduate]"),
  dict(name="lorry or bus licence", kind="credential", ways="R B", odds=0, skill_half=15, retires=None,
       ages=(18, 75), share=.03,   # estimate
       say="can drive a lorry",
       gained="a course paid for by an employer or out of [savings]",
       lost="a failed medical, a ban",
       needs="[driving licence]"),
  dict(name="trade ticket", kind="credential", ways="U B", odds=0, skill_half=15, retires=None,
       ages=(18, 80), share=.04,   # estimate: registered electricians, gas fitters and the like
       say="a registered tradesperson",
       gained="the end of an apprenticeship: 'earning a qualification'",
       lost="a lapsed registration, a serious fault found",
       needs="[apprentice]; [building trade]"),
  dict(name="hunting licence", kind="credential", ways="G B", odds=0, skill_half=15, retires=None,
       ages=(16, 90), share=.04,   # estimate: firearms or hunting licences
       say="holds a hunting licence",
       gained="a hunting club, a farm, a background check and a locked cabinet",
       lost="a conviction, a move to the city",
       needs="not [someone with a record]; [hunting and fishing]"),
  dict(name="motorbike licence", kind="credential", ways="R", odds=0, skill_half=15, retires=None,
       ages=(16, 85), share=.1,   # estimate
       say="rides a motorbike",
       gained="a test at sixteen or seventeen, or 'the itch to be somewhere else' at forty-five",
       lost="an accident, a ban, a partner's worry",
       needs="a basic training course"),
  dict(name="citizenship", kind="credential", ways="W B", odds=0, skill_half=None, retires=None,
       ages=(5, 110), share=.08,   # about 14 in 100 people are foreign-born and about 6 in 10 of them naturalise (OECD), so about 8 in 100 (2026-10-07; was .06)
       say="has citizenship",
       gained="years of residence, a test on the history and laws, an oath at a ceremony with a small flag",
       lost="almost never",
       needs="[immigrant]; years of legal residence"),
  dict(name="drinks licence", kind="credential", ways="B R", odds=0, skill_half=10, retires=None,
       ages=(18, 80), share=.03,   # estimate: a personal licence to sell alcohol, for running a pub or a shop
       say="holds a licence to sell drink",
       gained="a course and a police check before taking on a pub or an off-licence",
       lost="a bad night with the police called, or the business closing",
       needs="age 18, and no serious conviction"),
  dict(name="coaching badge", kind="credential", ways="R W", odds=0, skill_half=10, retires=None,
       ages=(16, 85), share=.05,   # estimate
       say="a qualified coach",
       gained="a weekend course run by the sport's association",
       lost="it lapses",
       needs="[on the team] once"),
  dict(name="referee's badge", kind="credential", ways="W", odds=0, skill_half=10, retires=None,
       ages=(14, 75), share=.03,   # estimate
       say="a qualified referee",
       gained="a course, a rule book learned by heart, and a first match where both sides shout",
       lost="it lapses; the knees go",
       needs="[on the team] once"),
]

# ---------- standing: how others see the person; it fades by skill_half once the person is gone from view
PERKS += [
  dict(name="good name in town", kind="standing", ways="W G", odds=.05, skill_half=10, retires=None,
       ages=(16, 110), share=.3,   # estimate
       say="has a good name in town",
       gained="years of 'kept your word' and 'helped someone in need' where people can see",
       lost="'a public scandal', 'a rumour about you' that sticks; moving away suspends it",
       needs="'kept your word' and 'helped someone in need' several times"),
  dict(name="rank", kind="standing", ways="W B", odds=.05, skill_half=10, retires=65,
       ages=(20, 67), share=.12,   # estimate: a sergeant, a ward sister, a foreman, a head of department
       say="holds a rank",
       gained="'a promotion is open' and years of service behind it",
       lost="demotion, a scandal, retirement",
       needs="a career title held for years; [reliable record]"),
  dict(name="known face at worship", kind="standing", ways="G W", odds=.03, skill_half=10, retires=None,
       ages=(6, 110), share=.2,   # estimate
       say="a known face at the mosque or church",
       gained="years at the same services, 'welcomed into a community'",
       lost="drifting away, a move",
       needs="[regular worshipper]"),
  dict(name="reliable record", kind="standing", ways="W", odds=.04, skill_half=8, retires=None,
       ages=(14, 100), share=.4,   # estimate
       say="known for turning up",
       gained="'kept your word' many times; years without a missed shift",
       lost="'broke your word' once at the wrong moment",
       needs="'kept your word' several times"),
  dict(name="good credit", kind="standing", ways="B W", odds=.04, skill_half=6, retires=None,
       ages=(18, 110), share=.6,   # estimate
       say="good for a loan",
       gained="bills paid on time, a first credit card handled well",
       lost="missed payments, 'financial ruin'",
       needs="age 18 and an income"),
  dict(name="the one everyone asks", kind="standing", ways="U G", odds=.04, skill_half=10, retires=None,
       ages=(25, 110), share=.2,   # estimate
       say="the one everyone asks",
       gained="'a grown child in the family asks for advice', 'years of practice are noticed'",
       lost="a big mistake, being proved wrong in public",
       needs="'learned a skill' many times"),
  dict(name="following online", kind="standing", ways="R B", odds=.04, skill_half=2, retires=None,
       ages=(13, 100), share=.04,   # estimate: tens of thousands of followers or more
       say="has a following online",
       gained="'wanting to be noticed', and a video that spreads overnight",
       lost="a year of silence, 'a public scandal'",
       needs="a phone and nerve"),
  dict(name="name in the field", kind="standing", ways="U B", odds=.06, skill_half=10, retires=None,
       ages=(25, 110), share=.05,   # estimate
       say="known in their field",
       gained="'a breakthrough in your work', 'honoured for your life's work'",
       lost="a scandal, being overtaken by the young",
       needs="a career title for years; 'learned a skill' many times"),
  dict(name="not to be crossed", kind="standing", ways="B R", odds=.04, skill_half=8, retires=None,
       ages=(12, 100), share=.05,   # estimate
       say="is not to be crossed",
       gained="'made an enemy' and come out on top; 'a fight after school' that went their way",
       lost="losing a fight in public, going soft",
       needs="'made an enemy' several times"),
  dict(name="regular at the local", kind="standing", ways="R G", odds=.03, skill_half=5, retires=None,
       ages=(18, 110), share=.3,   # estimate: the pub, the café, the barber's
       say="a regular at the local",
       gained="years at the same table; 'a new friend at the community centre'",
       lost="the place closing, a move",
       needs="'made a friend' there"),
  dict(name="local hero", kind="standing", ways="R W", odds=.04, skill_half=10, retires=None,
       ages=(10, 110), share=.02,   # estimate
       say="a local hero",
       gained="'a stranger saves you, or you save one', with a photo in the local paper",
       lost="people forget",
       needs="'helped someone in need' and 'took a wild risk' at once"),
  dict(name="old family name", kind="standing", ways="G B", odds=.04, skill_half=25, retires=None,
       ages=(0, 110), share=.08,   # estimate
       say="from an old family in the town",
       gained="born to it, or married into it",
       lost="a family scandal, a move far away",
       needs="a family that has lived there for generations"),
  dict(name="inner circle at work", kind="standing", ways="B U", odds=.05, skill_half=3, retires=70,
       ages=(25, 75), share=.08,   # estimate
       say="in the inner circle",
       gained="'your team lands a big contract', 'you are offered the top job'",
       lost="'someone tries to push you out at work', a new boss",
       needs="a career title; a [friend in power] helps"),
  dict(name="teachers' favourite", kind="standing", ways="U W", odds=.04, skill_half=3, retires=19,
       ages=(5, 19), share=.3,   # estimate
       say="a favourite with the teachers",
       gained="'a test at school tomorrow' passed, homework always in, a hand always up",
       lost="trouble at school ('you are grounded for a week' kind of trouble), a new school",
       needs="school"),
]

# ---------- bond: a person (or an animal) on the person's side; when the bond goes, what it taught fades by skill_half
PERKS += [
  dict(name="mentor", kind="bond", ways="U W", odds=.05, skill_half=20, retires=None,
       ages=(10, 90), share=.5,   # about 2 young Americans in 3 had a mentor of some kind (MENTOR, 2014); estimate for
                                  # one who counts
       say="has a mentor",
       gained="'a teacher or coach who believes in you'; an older hand at work who takes them under a wing",
       lost="the mentor dies, retires or moves on; the lessons stay",
       needs="'learned a skill' or 'helped someone in need'"),
  dict(name="friend in power", kind="bond", ways="B U", odds=.05, skill_half=5, retires=None,
       ages=(16, 110), share=.08,   # estimate
       say="has a friend in power",
       gained="a school friend who rose high, or 'made a friend' of the boss's boss",
       lost="the friend falls, or turns away",
       needs="'made a friend'"),
  dict(name="patron", kind="bond", ways="B R", odds=.06, skill_half=5, retires=None,
       ages=(14, 100), share=.02,   # estimate
       say="has a patron",
       gained="'an unexpected chance: a grant, a role, a stage', 'praise from a stranger' with money behind it",
       lost="a quarrel, the patron's death",
       needs="a gift worth backing; 'took a wild risk'"),
  dict(name="family who will always take you in", kind="bond", ways="G", odds=.04, skill_half=20, retires=None,
       ages=(0, 110), share=.7,   # estimate
       say="always has a home to go back to",
       gained="born to it; or 'making peace with family you had cut off'",
       lost="a deep break, or the old ones dying one by one",
       needs="a family"),
  dict(name="friend for life", kind="bond", ways="R G", odds=.04, skill_half=15, retires=None,
       ages=(6, 110), share=.6,   # estimate
       say="has a friend for life",
       gained="'a friend for life', who may have been 'a new kid joins your class' once",
       lost="'betrayed by a friend or a business partner', 'your closest friend dies'",
       needs="'made a friend'"),
  dict(name="old school network", kind="bond", ways="U B", odds=.04, skill_half=15, retires=None,
       ages=(18, 110), share=.15,   # estimate
       say="knows people from school",
       gained="a well-connected school or university, and a reunion every five years",
       lost="letting it go cold",
       needs="[graduate] or a school with a name"),
  dict(name="sponsor in recovery", kind="bond", ways="W G", odds=.05, skill_half=10, retires=None,
       ages=(16, 110), share=.03,   # estimate
       say="has a sponsor",
       gained="the first weeks at meetings after 'an addiction takes hold'",
       lost="the sponsor moves or relapses, and a new one is found",
       needs="[in recovery]"),
  dict(name="neighbour who has your back", kind="bond", ways="G W", odds=.03, skill_half=5, retires=None,
       ages=(16, 110), share=.4,   # estimate
       say="has a good neighbour",
       gained="'new people move in next door' and become friends; 'break-ins on the street' bring the street together",
       lost="a move, or 'a neighbour's dog keeps you awake' turned into a feud",
       needs="'made a friend' or 'helped someone in need'"),
  dict(name="contact in the trade", kind="bond", ways="B G", odds=.04, skill_half=5, retires=None,
       ages=(18, 90), share=.15,   # estimate
       say="has a contact in the trade",
       gained="years of work done well for the same people; 'someone you helped returns the favour'",
       lost="a falling-out, the contact retiring",
       needs="a career title"),
  dict(name="family abroad", kind="bond", ways="R U", odds=.03, skill_half=15, retires=None,
       ages=(0, 110), share=.2,   # estimate
       say="has family abroad",
       gained="a family spread over two countries; 'a long-lost relative finds you'",
       lost="the cousins die or drift",
       needs="relatives who once 'moved away'"),
  dict(name="old comrades", kind="bond", ways="R W", odds=.04, skill_half=15, retires=None,
       ages=(20, 110), share=.1,   # estimate: army mates, an old team, a crew that went through something together
       say="has old comrades",
       gained="years as a [soldier] or [on the team] in the same hard place",
       lost="deaths, quarrels",
       needs="[veteran], or years on a team"),
  dict(name="godparent who looks out", kind="bond", ways="W B", odds=.03, skill_half=10, retires=None,
       ages=(0, 60), share=.15,   # estimate
       say="has a godparent who looks out for them",
       gained="chosen by the parents at a christening or naming day",
       lost="a falling-out, the godparent's death",
       needs="parents who chose one"),
  dict(name="dog of one's own", kind="bond", ways="G R", odds=.02, skill_half=3, retires=None,
       ages=(4, 110), share=.4,   # estimate
       say="has a dog",
       gained="'a pet of your own', 'a stray dog follows you home'",
       lost="'your pet dies', a move to a flat that bans dogs",
       needs="a home that allows one, and money for food"),
  dict(name="in-laws who took you in", kind="bond", ways="R G", odds=.03, skill_half=10, retires=None,
       ages=(18, 110), share=.35,   # estimate
       say="has in-laws who treat them as their own",
       gained="'a holiday dinner with both families' that goes well; years of Sunday lunches",
       lost="a divorce, a row at a funeral",
       needs="[wife or husband] or [living together]"),
]

# ---------- asset: what the person owns; when it is gone it is gone (skill_half None)
PERKS += [
  dict(name="savings", kind="asset", ways="B W", odds=0, skill_half=None, retires=None,
       ages=(10, 110), share=.5,   # estimate: three months' pay or more put by, at some point in life
       say="has savings put by",
       gained="'a cushion of your own', saving from 'your first pocket money', 'money worries end'",
       lost="'a bill you did not expect', 'financial ruin', 'a sudden urge to buy something big'",
       needs="money left over at the end of the month"),
  dict(name="paid-off home", kind="asset", ways="G B", odds=0, skill_half=None, retires=None,
       ages=(35, 110), share=.45,   # estimate
       say="owns their home outright",
       gained="the last mortgage payment, or 'an unexpected legacy'",
       lost="'losing the home', 'moving to a smaller home or into care'",
       needs="[homeowner] for years"),
  dict(name="car", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(17, 100), share=.85,   # estimate: about 3 households in 4 have a car in England, more in the US
       say="has a car",
       gained="a first old banger bought with savings; 'a sudden urge to buy something big'",
       lost="a crash, 'money runs out at home', 'the doctor says to stop driving'",
       needs="[driving licence], and money for petrol"),
  dict(name="family business", kind="asset", ways="B W G", odds=0, skill_half=None, retires=None,
       ages=(14, 100), share=.07,   # estimate
       say="has the family business",
       gained="taken in by a relative who runs their own shop, or handed down at a parent's retirement",
       lost="'financial ruin', 'a dispute over an inheritance', selling up",
       needs="a family that owns one; [shop owner] or [farmer] often follows"),
  dict(name="inheritance", kind="asset", ways="G B U", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.4,   # estimate: a sum that changes something, not a keepsake
       say="has inherited money",
       gained="'a parent dies', then 'an unexpected legacy'",
       lost="spent, or lost to 'a dispute over an inheritance'",
       needs="a relative with something to leave"),
  dict(name="workplace pension", kind="asset", ways="W U", odds=0, skill_half=None, retires=None,
       ages=(22, 110), share=.7,   # estimate: most UK employees are now enrolled in one
       say="has a pension",
       gained="years in a job with a scheme; 'your pension statement arrives' every spring",
       lost="cashed in early, or a firm that goes under with it",
       needs="a career title for years"),
  dict(name="plot of land", kind="asset", ways="G", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.08,   # estimate: an allotment, a field, a farm
       say="has a plot of land",
       gained="'tending an allotment' after years on the waiting list; a field inherited",
       lost="selling up, giving it up when the knees go",
       needs="a waiting list, or money"),
  dict(name="shares", kind="asset", ways="B U", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.4,   # about 6 Americans in 10 own shares, many through pensions (Gallup 2023); fewer in
                                   # Europe
       say="has money invested",
       gained="'a bonus or a raise' put to work; 'a gamble that paid asks for another'",
       lost="'a recession', cashing out",
       needs="[savings]"),
  dict(name="van and tools", kind="asset", ways="R U", odds=0, skill_half=None, retires=None,
       ages=(18, 80), share=.08,   # estimate
       say="has a van and tools",
       gained="the first year of working for themselves",
       lost="theft, a crash, selling up at retirement",
       needs="[building trade] or [trade ticket]; [driving licence]"),
  dict(name="flat to rent out", kind="asset", ways="B", odds=0, skill_half=None, retires=None,
       ages=(25, 110), share=.06,   # about 1 adult in 20 in the UK lets out property (HMRC counts about 2.8 million
                                    # landlords); estimate
       say="a landlord",
       gained="an [inheritance] or years of [savings] turned into bricks",
       lost="selling, a tenant who wrecks it, a fall in prices",
       needs="[savings] or an [inheritance]; [good credit]"),
  dict(name="place by the sea", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(25, 110), share=.08,   # estimate: a second home or a holiday caravan
       say="has a place by the sea",
       gained="savings spent at last, or a grandparent's caravan handed down",
       lost="selling it when money is short",
       needs="[savings]"),
  dict(name="scholarship", kind="asset", ways="U W", odds=0, skill_half=None, retires=25,
       ages=(11, 30), share=.08,   # estimate
       say="on a scholarship",
       gained="'you win a scholarship or a place'",
       lost="grades that slip; graduating",
       needs="'learned a skill' several times; [school-leaving certificate] for a university one"),
  dict(name="workshop", kind="asset", ways="U G", odds=0, skill_half=None, retires=None,
       ages=(14, 110), share=.15,   # estimate: a shed or garage with real tools in it
       say="has a workshop",
       gained="a shed and years of birthday tools; a grandfather's bench",
       lost="a move to a flat, a house sale",
       needs="[fixing things]"),
  dict(name="instrument of one's own", kind="asset", ways="R U", odds=0, skill_half=None, retires=None,
       ages=(5, 110), share=.2,   # estimate
       say="has an instrument of their own",
       gained="a second-hand guitar for a birthday, or a piano that came with the house",
       lost="sold when money is short",
       needs="money, or a generous relative"),
]


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

# ---------- volume 2, credential: a licence, a certificate or a paper; it can be suspended or taken, and the skill under it stays
PERKS += [
  dict(name="airline pilot licence", kind="credential", ways="U W", odds=0, skill_half=10, retires=65,
       ages=(19, 65), share=.0015,   # the US counts about a quarter of a million holders of commercial and airline
                                     # transport pilot certificates (FAA airmen statistics); estimate for ever
       say="holds an airline pilot licence",
       gained="years of flight school paid with loans or [savings], or flying in the forces, then the airline exams, a "
              "type rating and 'a job interview' in a simulator; it comes with [commercial pilot]",
       lost="a failed medical after 'a heart attack or stroke' or 'a warning from the doctor', a conviction, or letting "
            "it lapse after 'a wave of layoffs at work'; airline flying ends at 65, and the hands still know how to fly",
       needs="a first-class medical; not [someone with a record]; age 19 or more"),
  dict(name="train driving licence", kind="credential", ways="W", odds=0, skill_half=8, retires=None,
       ages=(20, 70), share=.001,   # Britain has about 20,000 train drivers (ASLEF), about 1 adult in 2,500 at a time;
                                    # estimate for ever
       say="is licensed to drive trains",
       gained="a selection day, a year of training on the rules and the routes, then a licence in their own name; it "
              "comes with [train driver]",
       lost="a failed medical, a conviction, or leaving the cab; route knowledge fades fast",
       needs="age 20 or more; regular medicals; not [someone with a record] for most operators"),
  dict(name="seafarer's papers", kind="credential", ways="R G", odds=0, skill_half=15, retires=None,
       ages=(16, 70), share=.003,   # estimate: officers and crew of rich countries' fleets, and the cruise-ship and
                                    # yacht crews who need the same basic safety training
       say="has seafarer's papers",
       gained="basic safety training at a maritime college (fire, first aid, survival, the lifeboat drill), a seafarer "
              "medical and a discharge book; a cadetship as a [merchant seafarer], or a season on a cruise ship after "
              "'the itch to be somewhere else'",
       lost="a failed seafarer medical; they lapse after years ashore, often after 'an offer of work ashore'",
       needs="age 16 or more; good health; [swimming] helps"),
  dict(name="sea survival certificate", kind="credential", ways="W R", odds=0, skill_half=5, retires=None,
       ages=(16, 75), share=.006,   # estimate: Britain asks it of every new commercial fisher (Seafish), and offshore
                                    # oil and wind workers renew theirs every four years
       say="is trained in sea survival",
       gained="a day in a training pool in a survival suit, righting a life raft and climbing in from the water; it "
              "comes with [commercial fisher], [lifeboat volunteer] and [merchant seafarer], and offshore work asks "
              "for it too",
       lost="it lapses four or five years after the course unless refreshed; leaving the sea lets it go",
       needs="a course paid by the boat, the station or an employer; [swimming] helps"),
  dict(name="fishing licence", kind="credential", ways="G R", odds=0, skill_half=15, retires=None,
       ages=(12, 100), share=.15,   # the US sells fishing licences to about 30 million people a year (US Fish and
                                    # Wildlife Service); England about a million rod licences (Environment Agency);
                                    # estimate for ever
       say="holds a fishing licence",
       gained="a rod licence bought at the post office or online, after a grandparent's river at dawn ([hunting and "
              "fishing]) or 'a day at the beach' with a borrowed line; a commercial permit for a [commercial fisher]",
       lost="not renewed one spring; a ban after an offence",
       needs="age 12 or 13 or more for a rod licence; a permit and a quota for commercial fishing"),
  dict(name="gas safety registration", kind="credential", ways="U B", odds=0, skill_half=10, retires=None,
       ages=(18, 75), share=.004,   # UK: about 130,000 engineers on the Gas Safe Register; US states license gas
                                    # fitters; estimate
       say="is registered to work on gas",
       gained="assessed on boilers and pipework after years as a [plumber] or a heating engineer, then a photo card "
              "and a number on the register",
       lost="a dangerous job found on inspection; the yearly registration let go after leaving the trade",
       needs="[trade ticket] or years as a [plumber]; an assessment every five years"),
  dict(name="welding certificate", kind="credential", ways="R W B", odds=0, skill_half=10, retires=None,
       ages=(16, 75), share=.008,   # the US counts over 400,000 welders, cutters, solderers and brazers (BLS), and
                                    # pipefitters and fabricators hold them too; estimate
       say="holds a welding certificate",
       gained="a test plate cut, bent and X-rayed after a course or an [apprentice] place; each certificate names a "
              "process and a position, and it comes with [welder]",
       lost="it lapses after six months without welding to that code; the hands keep the skill",
       needs="a welding course or an apprenticeship; 'learned a skill' several times"),
  dict(name="food hygiene certificate", kind="credential", ways="W G", odds=0, skill_half=5, retires=None,
       ages=(14, 90), share=.25,   # estimate: food work is one of the commonest first jobs; EU law requires food
                                   # handlers to be trained (Regulation 852/2004), and many US states ask for a food
                                   # handler card
       say="has a food hygiene certificate",
       gained="an afternoon's course and a short test before the first shift in a kitchen, a bakery or a care home; "
              "it comes with [cook], [baker] and [community-kitchen volunteer]",
       lost="it goes out of date after about three years away from food work; the habit of washing hands stays",
       needs="'your first real job' or 'a Saturday job at the corner shop' with food on the counter, or a place on a "
             "volunteer rota"),
  dict(name="tattoo licence", kind="credential", ways="R B", odds=0, skill_half=10, retires=None,
       ages=(18, 80), share=.0015,   # estimate: tattooists and cosmetic tattooists registered with a council or a
                                     # state health department
       say="is licensed to tattoo",
       gained="a hygiene course, an inspection of the studio and a registration in the artist's own name; it comes "
              "with [tattoo artist]",
       lost="a failed hygiene inspection, or letting it lapse after leaving the trade",
       needs="age 18 or more; [drawing and painting]; a studio that passes inspection"),
  dict(name="celebrant authorisation", kind="credential", ways="R W", odds=0, skill_half=10, retires=None,
       ages=(18, 95), share=.015,   # estimate: Australia has several thousand authorised marriage celebrants
                                    # (Attorney-General's Department); in the US many couples are married by a friend
                                    # ordained online; in most of Europe only registrars and clergy marry people
       say="is authorised to conduct weddings",
       gained="a celebrant course and a place on the state's register, which comes with [civil celebrant]; ordination "
              "for an [ordained religious minister]; in some places a one-day designation, or an online "
              "ordination, to lead a friend's wedding after 'dancing at a wedding' many times",
       lost="struck from the register after a conviction, or the yearly training let go",
       needs="age 18 or more; legal recognition where the country gives it; [public speaking] helps"),
  dict(name="court interpreter accreditation", kind="credential", ways="W U", odds=0, skill_half=10, retires=None,
       ages=(23, 80), share=.0005,   # estimate: Britain's register of public service interpreters lists a few
                                     # thousand (NRPSI)
       say="is accredited to interpret in court",
       gained="an interpreting exam, a background check and an oath before the court; in many places the same oath "
              "lets a [translator] certify official papers; it comes with [court interpreter]",
       lost="a conviction, a complaint upheld, or letting it lapse after leaving the work",
       needs="[second language] at a professional level; not [someone with a record]; age 23 or more"),
  dict(name="chartered status", kind="credential", ways="U B", odds=0, skill_half=10, retires=None,
       ages=(25, 85), share=.006,   # the UK Engineering Council registers well over 100,000 Chartered Engineers; the
                                    # US licenses nearly half a million professional engineers (NSPE); estimate with
                                    # chartered surveyors and planners
       say="holds chartered status",
       gained="years of supervised work as a [civil engineer], a [land surveyor], an [architect] or an [urban "
              "planner], a written case and a professional review; letters after the name",
       lost="struck off after a complaint upheld, or resigned at retirement; the knowledge stays",
       needs="[graduate] or the [apprentice] route; four years or more in the work"),
  dict(name="rigging ticket", kind="credential", ways="R U", odds=0, skill_half=8, retires=None,
       ages=(18, 70), share=.006,   # estimate: stage and arena riggers are few; crane slingers and signallers on
                                    # building sites far more
       say="holds a rigging ticket",
       gained="a course in harnesses, hoists and load charts after a first year as a [stage technician], or on a "
              "building site as a slinger for [builder] and [welder] crews",
       lost="it lapses unless renewed every few years; a fall or a fault found ends the work at height",
       needs="a head for heights; a [site safety card] for building sites"),
  dict(name="press card", kind="credential", ways="U R", odds=0, skill_half=5, retires=None,
       ages=(18, 85), share=.004,   # estimate: about as many as work as journalists for a while
       say="carries a press card",
       gained="a first year of paid work as a [journalist], vouched for by an editor or a union",
       lost="handed back after leaving journalism; it must be renewed every few years",
       needs="[journalist]; work published or broadcast"),
  dict(name="therapy accreditation", kind="credential", ways="U G", odds=0, skill_half=15, retires=None,
       ages=(25, 85), share=.005,   # estimate: the US counts several hundred thousand licensed counsellors and family
                                    # therapists (BLS); Britain's counselling bodies have tens of thousands of members
       say="is accredited to practise therapy",
       gained="years of supervised clinical hours, therapy of their own and a panel's review; it comes with "
              "[psychotherapist], and some [nurse] and [teacher] careers turn to counselling this way",
       lost="struck off after a complaint upheld, or let go at retirement; what it taught stays",
       needs="[graduate]; a recognised training and supervision; not [someone with a record]"),
  dict(name="mediation accreditation", kind="credential", ways="W G", odds=0, skill_half=10, retires=None,
       ages=(21, 90), share=.005,   # estimate: community, family, workplace and court mediators
       say="is an accredited mediator",
       gained="a forty-hour course, role plays and supervised cases; it comes with [community-mediation volunteer], "
              "and a [restorative-justice advocate] trains this way to run a meeting",
       lost="it lapses without supervised cases and refresher hours",
       needs="[calming people down]; impartiality; age 21 or more"),
  dict(name="cleared to work with children", kind="credential", ways="W", odds=0, skill_half=None, retires=None,
       ages=(16, 95), share=.25,   # estimate: England's Disclosure and Barring Service issues several million
                                   # certificates a year; in Australia's states a working-with-children check is held
                                   # by a large minority of adults
       say="is cleared to work with children",
       gained="a background check for a first job or a volunteer role with children: as a [teacher], a [youth coach], "
              "a [school-governance board member], a [lay religious teacher] or a parent helper on the school trip",
       lost="a new conviction that shows on the check; otherwise it goes with the role and is renewed with the next",
       needs="age 16 or more; a role that asks for it; not [someone with a record] for most roles"),
  dict(name="site safety card", kind="credential", ways="W B", odds=0, skill_half=5, retires=None,
       ages=(16, 75), share=.1,   # UK: about 2 million CSCS cards in circulation (CSCS); US: OSHA's outreach courses
                                  # train about a million workers a year; estimate for ever
       say="has a site safety card",
       gained="a health and safety test before the first day on a building site, often as an [apprentice] or a "
              "[builder]; a [carpenter], a [welder] and a [civil engineer] carry one too",
       lost="it runs out after five years off the sites",
       needs="age 16 or more; a short course and a test"),
  dict(name="lifeguard qualification", kind="credential", ways="W R", odds=0, skill_half=5, retires=None,
       ages=(16, 70), share=.03,   # estimate: a common summer job for teenagers; pool lifeguard awards are renewed
                                   # every two years
       say="is a qualified lifeguard",
       gained="a pool course at sixteen or seventeen (towing a dummy, spinal holds, resuscitation), then 'your first "
              "real job' on the poolside or the beach; some go on to be a [lifeboat volunteer]",
       lost="it lapses after two years without requalifying, and the rescue drills fade",
       needs="[swimming], and strong; age 16 or more; a [first-aid certificate] comes with it"),
  dict(name="diving certificate", kind="credential", ways="R U", odds=0, skill_half=10, retires=None,
       ages=(10, 85), share=.04,   # PADI alone has issued close to 30 million certifications since 1967 (PADI), many to
                                   # holidaymakers from rich countries; estimate
       say="is a certified diver",
       gained="a week's course on 'a long-planned trip' or in a cold quarry at home: the classroom, the pool, then four "
              "open-water dives; some [archaeologist] and [search-and-rescue volunteer] teams dive",
       lost="it never lapses, though years out of the water mean a refresher first",
       needs="[swimming]; age 10 or more; a medical form"),
  dict(name="reader's ticket", kind="credential", ways="U G", odds=0, skill_half=15, retires=None,
       ages=(16, 110), share=.03,   # estimate: national libraries and record offices register many thousands of new
                                    # readers a year, family historians most of them
       say="holds a reader's ticket to the archives",
       gained="proof of address and a reason to look, at a national library or a county record office: family history "
              "after 'a parent dies', a thesis, a book; an [archivist] often starts in the reading room",
       lost="it expires and is renewed at the next visit",
       needs="age 16 or 18 or more; [finding things out] helps"),
  dict(name="permanent residence", kind="credential", ways="G B", odds=0, skill_half=None, retires=None,
       ages=(0, 110), share=.08,   # estimate: foreign-born people are about 14% of the population across rich OECD
                                   # countries (OECD), and most who stay are settled; the US counts about 13 million
                                   # green-card holders (DHS)
       say="has permanent residence",
       gained="years of legal residence as an [immigrant], or protection given to a [refugee] and later made "
              "permanent: a card that says the person may stay",
       lost="replaced by [citizenship], or given up on going home as a [returned migrant]; long years abroad can end "
            "it",
       needs="[immigrant]; years of legal residence, a clean record and the fee"),
  dict(name="chainsaw ticket", kind="credential", ways="G U", odds=0, skill_half=10, retires=None,
       ages=(16, 85), share=.015,   # estimate: forestry, tree and farm work ask for one in Britain; in Germany people
                                    # who cut their own firewood in a state forest take the course
       say="holds a chainsaw ticket",
       gained="a week's course on upkeep and felling, then an assessment in the woods; it comes with [forester], and "
              "a [farmer] or a tree surgeon needs one too",
       lost="it does not lapse, but insurers want a refresher after years away",
       needs="age 16 or more; protective kit"),
]

# ---------- volume 2, standing: how others see the person; it fades by skill_half once the person is gone from view
PERKS += [
  dict(name="book in print", kind="standing", ways="R U", odds=.04, skill_half=20, retires=None,
       ages=(16, 110), share=.01,   # estimate: authors of a book from a publisher, academic and local history books
                                    # included
       say="has a book in print",
       gained="a first published book as a [novelist], a history of the town, a [doctoral graduate]'s thesis turned "
              "into a book; 'the notebooks come together'",
       lost="the book going out of print and out of mind",
       needs="[writing stories] or a subject; a publisher"),
  dict(name="published research", kind="standing", ways="U W", odds=.05, skill_half=15, retires=None,
       ages=(22, 110), share=.015,   # OECD: about 9 researchers per 1,000 people in work (Main Science and Technology
                                     # Indicators); estimate for those who ever publish
       say="has published research",
       gained="a thesis as a [doctoral graduate], papers from the bench as a [laboratory technician] or from a dig as "
              "an [archaeologist]; 'a breakthrough in your work'",
       lost="a paper withdrawn; being overtaken by the young",
       needs="[graduate]; [lab work] or [archive research] often"),
  dict(name="loyal clientele", kind="standing", ways="B", odds=.05, skill_half=2, retires=None,
       ages=(18, 90), share=.06,   # estimate: about 1 worker in 7 in the EU is self-employed (Eurostat); fewer keep
                                   # regulars who follow them
       say="has a loyal clientele",
       gained="years of good work as a [tattoo artist], a [baker], a [plumber] or a [civil celebrant]; "
              "'a client asks to cut out the agency'",
       lost="giving up the work, a move away from the clients",
       needs="a career title for years; [reliable record] helps"),
  dict(name="award for bravery", kind="standing", ways="W R", odds=.03, skill_half=25, retires=None,
       ages=(8, 110), share=.004,   # estimate: medals and commendations from the services and the humane societies,
                                    # a few thousand a year in a large country
       say="has an award for bravery",
       gained="'a stranger saves you, or you save one', on a shout as a [firefighter] or a [lifeboat volunteer], or "
              "off duty; a ceremony and a framed certificate",
       lost="only 'a public scandal'",
       needs="'helped someone in need' and 'took a wild risk' at once"),
  dict(name="voice at the town hall", kind="standing", ways="W B", odds=.05, skill_half=4, retires=None,
       ages=(18, 110), share=.02,   # estimate: the people the council phones before it decides
       say="has a voice at the town hall",
       gained="years as a [school-governance board member], a [neighbourhood-watch coordinator] or a "
              "[disability-rights organiser]; 'your town faces a change you could fight'",
       lost="a move, 'a public scandal', 'a bitter election'",
       needs="[good name in town] or a cause; years in the same place"),
  dict(name="name on the local scene", kind="standing", ways="R G", odds=.04, skill_half=5, retires=None,
       ages=(16, 100), share=.03,   # estimate: music, food, art and clubs in one town
       say="a name on the local scene",
       gained="years of gigs as an [amateur band member], a [festival organiser]'s street party, a weekly show as a "
              "[community-radio presenter]",
       lost="a move to a new town; the scene moving on without them",
       needs="'made a friend' several times"),
  dict(name="trusted with the keys", kind="standing", ways="W G", odds=.03, skill_half=5, retires=None,
       ages=(18, 110), share=.2,   # estimate: keyholders of a hall, a church, a club or a neighbour's house, and of a shop or site at work (was .12)
       say="is trusted with the keys",
       gained="years as a [cleaner], a [club treasurer] or a [deacon or elder]; 'kept your word' where people could see",
       lost="'broke your word' or 'hid a wrong', found out; a move",
       needs="[reliable record]"),
  dict(name="trophies won", kind="standing", ways="R B", odds=.03, skill_half=20, retires=None,
       ages=(8, 110), share=.05,   # estimate: county, league and national titles, not a medal for taking part
       say="has trophies to their name",
       gained="seasons [on the team], 'the Saturday team wins at last', years as a [professional athlete] or in "
              "[boxing or martial arts]",
       lost="people forget",
       needs="'tryouts for the team' passed"),
]

# ---------- volume 2, bond: a person (or an animal) on the person's side; when the bond goes, what it taught fades by skill_half
PERKS += [
  dict(name="crew that has your back", kind="bond", ways="R W", odds=.05, skill_half=10, retires=None,
       ages=(16, 80), share=.12,   # estimate: a watch, a boat's crew, a kitchen brigade, a stage crew, a site gang
       say="has a crew that has their back",
       gained="a watch as a [firefighter], a crew as a [lifeboat volunteer], a [merchant seafarer] or a "
              "[stage technician], a kitchen as a [head chef]; 'a narrow escape' together",
       lost="leaving the job, the crew breaking up; what is left becomes [old comrades]",
       needs="work done together in danger or under pressure"),
  dict(name="apprentice of one's own", kind="bond", ways="U G", odds=.03, skill_half=15, retires=None,
       ages=(25, 85), share=.04,   # estimate: tradespeople and craftspeople who train an apprentice through to the end
       say="has an apprentice of their own",
       gained="years as a [machinist], a [welder], a [carpenter], a [baker] or a [tattoo artist]; "
              "'a younger colleague needs a mentor'",
       lost="the apprentice qualifies and goes their own way; what teaching taught stays",
       needs="a trade held for years; [teaching] helps"),
  dict(name="carers' group", kind="bond", ways="G W", odds=.04, skill_half=5, retires=None,
       ages=(16, 110), share=.03,   # England and Wales: about 5 million unpaid carers (Census 2021); estimate for those
                                    # who find a group
       say="has a carers' group to lean on",
       gained="'a week off from caring' found through other carers; years as a [carer for a parent], a "
              "[caregiving partner] or a [parent coordinating complex support needs]",
       lost="the caring years ending; the group folding",
       needs="a caring role"),
  dict(name="source who trusts you", kind="bond", ways="U B", odds=.04, skill_half=3, retires=None,
       ages=(18, 95), share=.005,   # estimate
       say="has a source who trusts them",
       gained="years of 'kept your word' as a [journalist] or a [civil-liberties campaigner]; "
              "'a story nobody in town has covered'",
       lost="'broke your word' once; leaving the work",
       needs="[reporting]; 'kept your word'"),
  dict(name="business partner", kind="bond", ways="B R", odds=.05, skill_half=5, retires=None,
       ages=(18, 90), share=.06,   # estimate: partnerships and co-founded firms
       say="has a business partner",
       gained="'a friend wants to start a project with you', 'a chance to start a business of your own' as a "
              "[founder of a firm] or a [shop owner]",
       lost="'betrayed by a friend or a business partner', 'financial ruin', selling up",
       needs="'made a friend'; 'took a wild risk'"),
  dict(name="godchild", kind="bond", ways="W G", odds=.02, skill_half=15, retires=None,
       ages=(16, 100), share=.2,   # estimate: christenings and naming days are rarer than they were
       say="has a godchild",
       gained="asked at a christening or a naming day by a sister, a brother or a [friend for life]",
       lost="a falling-out with the parents, a move far away",
       needs="[friend for life] or family who ask"),
  dict(name="cat of one's own", kind="bond", ways="U G", odds=.02, skill_half=3, retires=None,
       ages=(4, 110), share=.45,   # about 1 UK adult in 4 owns a cat (PDSA, PAW Report 2024), about 1 US household in 3
                                   # (APPA); estimate over a life
       say="has a cat",
       gained="'a pet of your own', a kitten from a neighbour, a cat from the shelter of an [animal-shelter campaigner]",
       lost="'your pet dies'; a move to a flat that bans pets",
       needs="a home that allows one"),
  dict(name="people from home", kind="bond", ways="G B", odds=.04, skill_half=5, retires=None,
       ages=(16, 110), share=.08,   # estimate: immigrants and incomers who find their own people in a new city
       say="has people from home nearby",
       gained="'moved away' to a new city, a shop that sells the food of home, 'welcomed into a community' of others "
              "who came as an [immigrant] or a [refugee]",
       lost="another move; 'came home'",
       needs="'moved away', or [immigrant]"),
]

# ---------- volume 2, asset: what the person owns; when it is gone it is gone (skill_half None)
PERKS += [
  dict(name="hives of one's own", kind="asset", ways="G U", odds=0, skill_half=None, retires=None,
       ages=(14, 100), share=.005,   # estimate: the EU counts about 600,000 beekeepers (European Commission), and many
                                     # give up after a few seasons
       say="has hives of their own",
       gained="'a new hobby you cannot put down': a course with the local beekeepers, a swarm caught in a box or a "
              "colony bought in spring, and a registration with the bee inspector; a [professional beekeeper] grows "
              "from here",
       lost="'a third of the hives dead after winter' and not started again; a move with nowhere to keep them; old "
            "age and heavy boxes",
       needs="a garden, a [plot of land] or a farmer's corner where they may stand; neighbours who do not mind"),
  dict(name="boat of one's own", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(16, 100), share=.08,   # estimate: about 1 US household in 10 owns a boat (NMMA); Sweden counts close to
                                    # 900,000 leisure boats for 10 million people; far fewer in Britain
       say="has a boat of their own",
       gained="a second-hand dinghy, a fishing boat on a trailer or a narrowboat bought with [savings] after summers "
              "of 'a day at the beach'",
       lost="sold when money is short, or left to rot on the hard",
       needs="money for the mooring; [swimming] helps"),
  dict(name="share in a fishing boat", kind="asset", ways="G B", odds=0, skill_half=None, retires=None,
       ages=(18, 85), share=.0005,   # estimate: most fishing boats in rich countries belong to their skippers or to
                                     # families
       say="has a share in a fishing boat",
       gained="years as crew for a [commercial fisher], then a share bought with [savings] or an [inheritance], or "
              "handed down in a [family business]; the quota comes with it",
       lost="sold on leaving the sea, or to pay debts after 'financial ruin'; a fishery closed",
       needs="[commercial fisher] for some years; money or family"),
  dict(name="studio of one's own", kind="asset", ways="R B", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.015,   # estimate
       say="has a studio of their own",
       gained="a rented room with a lock and good light, a garage turned into a recording room, or a chair and a "
              "lease when a [tattoo artist] or a [sound engineer] sets up alone",
       lost="the rent goes up, the building is sold, a move",
       needs="rent money; [drawing and painting], [musical instrument] or a trade to practise there"),
  dict(name="premises of one's own", kind="asset", ways="B W", odds=0, skill_half=None, retires=None,
       ages=(20, 90), share=.04,   # estimate: owners and leaseholders of shops, cafes, practices and workshop units
       say="has premises of their own",
       gained="'a chance to start a business of your own': a lease signed on a shop, a surgery or a workshop unit, "
              "for a [shop owner], a [baker], a [funeral director] or a [veterinarian] in a practice of their own",
       lost="'financial ruin', 'a recession', a lease not renewed, selling up",
       needs="[savings] or a loan, and [good credit]"),
  dict(name="horse of one's own", kind="asset", ways="G R", odds=0, skill_half=None, retires=None,
       ages=(6, 90), share=.025,   # estimate: Britain's equestrian surveys count a few hundred thousand horse-owning
                                   # households (BETA); a childhood pony counts
       say="has a horse of their own",
       gained="a pony that came with a farm childhood, or years of riding lessons and then a horse bought or taken "
              "on loan at a livery yard",
       lost="the horse grows old and dies; sold when money is short",
       needs="money for livery, feed and the vet; a [plot of land] or a yard nearby"),
  dict(name="good telescope", kind="asset", ways="U R", odds=0, skill_half=None, retires=None,
       ages=(10, 110), share=.02,   # estimate
       say="has a good telescope",
       gained="saved up for after 'more stars than anyone could count' on a dark night, or bought second-hand from a "
              "club member on becoming an [amateur astronomer in a club]",
       lost="sold, or left in the loft after a move to the city lights",
       needs="money, and a garden or a dark hill to set it up on"),
  dict(name="period kit", kind="asset", ways="G U", odds=0, skill_half=None, retires=None,
       ages=(14, 90), share=.005,   # estimate: about as many as ever reenact, and a few who sew for them
       say="has period kit",
       gained="a first season in borrowed clothes, then winter evenings of sewing, a pair of shoes made to order and "
              "a market stall for the rest, as a [historical reenactment member]",
       lost="sold to a newcomer, or outgrown in the loft",
       needs="[historical reenactment member]; [sewing and mending] helps; money"),
  dict(name="stake in the firm", kind="asset", ways="B", odds=0, skill_half=None, retires=None,
       ages=(25, 85), share=.03,   # estimate: partners in practices and co-owners of small firms; employee share
                                   # schemes count only where they carry a say
       say="has a stake in the firm",
       gained="made a partner after years in a practice, as a [physician] in a group surgery, a [pharmacist], an "
              "[architect] or an [accountant]; or a buy-in to a [family business] or the firm a [founder of a firm] "
              "started",
       lost="bought out on leaving or retiring; 'financial ruin' if the firm fails",
       needs="a career title for years; money to buy in, or a firm that offers it"),
  dict(name="research grant", kind="asset", ways="U B", odds=0, skill_half=None, retires=None,
       ages=(23, 80), share=.008,   # estimate: researchers who lead a funded project of their own
       say="has a research grant",
       gained="a proposal written over a winter, then 'an unexpected chance: a grant, a role, a stage' when it is "
              "funded; the work of a [doctoral graduate], an [archaeologist], a [museum curator] or a [professional "
              "conservator] runs on them",
       lost="'the grant runs out in June'; the money is spent and the next proposal is turned down",
       needs="[graduate], usually a doctorate; an institution to hold the money"),
  dict(name="collection of one's own", kind="asset", ways="G B", odds=0, skill_half=None, retires=None,
       ages=(12, 110), share=.05,   # estimate: a collection worth something and known to others
       say="has a collection of their own",
       gained="years of fairs, auctions and attics (records, stamps, coins, old tools or books) after 'a curiosity "
              "that will not let go', or 'an unexpected legacy' of a grandparent's cabinet",
       lost="sold in hard times, split in 'a dispute over an inheritance', or given to a museum where a [museum "
            "curator] or a [professional conservator] looks after it",
       needs="space, patience and some money"),
  dict(name="tools of one's own", kind="asset", ways="U B", odds=0, skill_half=None, retires=None,
       ages=(16, 85), share=.08,   # estimate: about as many as have a trade in their hands ([building trade] .1), and
                                   # mechanics and serious amateurs with a kit worth insuring
       say="has tools of their own",
       gained="a first set bought with the first wages as an [apprentice] and added to for years; a [carpenter], a "
              "[welder] or a [plumber] works with their own",
       lost="stolen from the van, sold at retirement, handed on to a younger hand",
       needs="[building trade] or another trade; money"),
  dict(name="camper van", kind="asset", ways="R B", odds=0, skill_half=None, retires=None,
       ages=(21, 95), share=.05,   # estimate: about 11 million US households own a recreational vehicle (RV Industry
                                   # Association); fewer in Europe
       say="has a camper van",
       gained="'a late chance to see the world' or 'the itch to be somewhere else': a van fitted out over a winter, "
              "or a motorhome bought when 'the children leave home' and a [parent of independent adult children] has "
              "time again",
       lost="sold in hard times, or when 'the doctor says to stop driving'",
       needs="[driving licence]; money, and somewhere to park it"),
  dict(name="secure tenancy", kind="asset", ways="G W", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.12,   # estimate: about 1 household in 6 in England rents from a council or a housing
                                    # association (English Housing Survey), nearer 1 in 3 in the Netherlands and
                                    # Austria; far fewer in the US
       say="has a secure tenancy",
       gained="years on the council's waiting list, or a flat through a housing association after being [homeless] "
              "or 'losing the home'; a [housing-cooperative member] holds one through the cooperative; sometimes "
              "passed on from a parent",
       lost="'buying a home', a move away, or eviction after months of arrears",
       needs="a low income or a housing need, a local connection, and years on the list"),
]
