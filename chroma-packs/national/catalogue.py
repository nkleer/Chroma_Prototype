# Chroma content pack: National standing (modern Earth, with the tribal and magic worlds). Catalogue: the ten new
# national seats and the fifteen routes' assets. Pathways and packs thread, 2026-10-23, for v25: Emren's decision #11
# ("Fifteen routes and reusable combination styles", chroma-ideas/next-table-2026-10-19/v25-decisions-emren.md section
# 10) and Outer world's seat list (chroma-world/spheres/world-fit-v1.md section 3, data/world_fit.json "national").
# Plain data in the fields of chroma-library/earth_perks_titles.py (its header defines every field); nothing is
# imported and nothing runs. Modern Earth terms; the forms in the tribal and magic worlds are in worlds.py.
#
# SWITCHED OFF: `national` is not in batch.PACKS, so nothing reads this folder and no life changes. Leaving it out is
# the clean cut for national standing (cut-order item 3, v25-operation.md): with the pack off, the five seats that
# already exist (head of government, minister and party leader in politics; magnate and general in callings) are as
# v24 has them, and none of the routes' assets or moments exists.
#
# Why: no v24 life reached national standing. Only five titles give it (standing=3), all in rule, prot or comm and led
# by W, R or B. The fifteen routes of decision #11 each end in one national seat, three per colour, so every sphere has
# a seat and every colour leads three. The seats map one to one onto the routes (PACK.md, "The fifteen routes"):
#   W  Mandate Builder: head of government | Public Service Architect: minister | Common-Ground Maker: head of a
#      national faith body (new)
#   U  Discoverer: chief scientist (new) | Systems Inventor: director of a national laboratory (new) | Truthfinder:
#      editor of a national paper (new)
#   B  Enterprise Builder: magnate | Coalition Builder: head of a national industry body (new) | Opportunity Patron:
#      head of a national bank or exchange (new)
#   R  Rallying Voice: party leader | National Virtuoso: celebrated star of stage or sport (new) | Commander: general
#   G  Living-Land Steward: head of the national parks (new) | Living-Heritage Keeper: keeper of the national heritage
#      (new) | Community Weaver: head of a national charity (new)
# Three of Outer world's draft names changed to fit the routes (Vision agreed, 10-23 15:57): "national laureate"
# became "editor of a national paper" (the base [journalist] sits in gather); "leader of a national movement" became
# "keeper of the national heritage" (the engine's movement road already takes a movement's leader to national
# standing, and the Rallying Voice is the party leader); "director of a national laboratory or library" narrowed to
# the laboratory (the library and the museum are the heritage keeper's).
#
# Colour balance: each seat's ways are Outer world's pair, and its three profiles are that pair, a second pair and the
# fifth colour alone. Each colour is that single profile of exactly two seats, so the ten seats are exactly even (W U B
# R G 6.00 each; check_pack.py). The fifteen assets are one per route: each colour holds one standing, one bond and one
# asset, so the perks are exactly even too and every kind holds all five colours. A colour label says which route a
# colour covers, never who may climb it: every colour can hold every seat.
#
# Recognition, influence and formal authority are kept apart (decision #11; Outer world's world-fit-v2.md section 3).
# Authority is a seat: standing 3, the 8 to 12 national decisions a year, while it is held. Recognition is the shared
# reach ladder ([known across the country], [a household name], core/reach.py): one way into a seat among others, and
# never given by one. Influence is the route's asset (4 to 8 national proposals a year in the Engine's lane D): earned
# on the route or in the seat, kept after it while its obligation is kept. The routes' encounters (about 60, and 40 for
# the styles) are the Library's; the routes' data and the 20 styles are Outer world's (world_fit.json "national").
#
# Shares: the share of people in a modern rich country who ever hold the seat. A country has one or a few of each
# seat, held for 5 to 15 years, so these are a few in a million; every share is an estimate and says how it was
# reached. The game's targets for national standing (.01 to .03 of lives left alone, other-shapes.md) are the
# Engine's calibration of its smaller worlds, not these shares. Real names stay in these comments: the moments never
# name a real person, body, paper, bank, park, faith or country.
#
# The outer world's keywords (chroma-engine/world-fields.md, W38 and W40): sector=, institution= (an INST_KINDS value)
# and standing=3 on every seat; sphere= and face= on every title. The parks seat sits in prod with face prod.G (the land
# has no sphere of its own; Outer world's default, 10-21).
# The pack builds on these packs' titles (refines, needs and the routes' lower rungs) and is switched on only with
# them: callings is still off in v24, so the national pack waits for it (check_pack.py reads DEPENDS).
DEPENDS = ["politics", "callings", "science", "stage", "art"]

TITLES = []
PERKS = []

# ---------------------------------------------------------------- W: Common-Ground Maker (sphere faith)
TITLES += [
  dict(name="head of a national faith body", kind="faith", institution="faith body", standing=3, sphere="faith",
       face="faith.W", ways="W G", refines="head of a faith order; senior cleric",
       profiles=[("W G", "Keeps a whole faith together through its councils, its feasts and its long patience."),
                 ("U R", "Argues the hard questions out in the open, and will not let the faith hide from them."),
                 ("B", "Knows where every vote on the council lies, and spends that knowledge to keep the peace.")],
       meets="need:meaning+.12 need:belonging+.05 res:ties+.05 res:time-.15 res:freedom-.08",
       ages=(45, 90), share=.000003,   # estimate: the heads of a country's faith bodies and their national councils,
                                       # a few dozen at a time, most serving 7 to 15 years
       say="the head of a national faith body",
       gained="chosen by the faith's councils after years as a [head of a faith order] or a [senior cleric], often with "
              "[standing with both sides] or [known across the country]",
       lost="stepping down; the end of a term; a split in the faith",
       needs="[senior cleric] or [head of a faith order] for years; the trust of more than one side of the faith",
       turning="Two halves of the faith each want the head to stand with them, and a settlement means giving up "
               "something one of them holds sacred."),
]

# ---------------------------------------------------------------- U: Discoverer, Systems Inventor, Truthfinder
TITLES += [
  dict(name="chief scientist", kind="career", sector="public", institution="ministry", standing=3, sphere="learn",
       face="learn.U", ways="U W", refines="professor; research group leader; research facility lead",
       profiles=[("U W", "Tells the government what the evidence says, and how sure anyone can be of it."),
                 ("B G", "Builds the country's science for the long haul: the funds, the stations, the next generation."),
                 ("R", "Says the uncomfortable finding out loud, before the cabinet is ready to hear it.")],
       meets="need:meaning+.1 need:competence+.08 res:time-.15 res:freedom-.08",
       ages=(45, 75), share=.0000005,   # estimate: a government's chief scientific adviser and the chief scientists
                                        # of its ministries, about 20 at a time, each for about 5 years
       say="the country's chief scientist",
       gained="appointed by the government after years as a [professor], [research group leader] or "
              "[research facility lead]",
       lost="the end of the appointment; a quarrel with the government in public; retirement",
       needs="[professor], [research group leader] or [research facility lead] for years; [name in the field]",
       turning="The finding would change what the country does tomorrow, and it is not yet certain."),
  dict(name="director of a national laboratory", kind="career", sector="knowledge", institution="university",
       standing=3, sphere="learn", face="learn.U", ways="U B",
       refines="research facility lead; research group leader; celebrated inventor",
       profiles=[("U B", "Runs the country's great machines, and decides what gets built on them next."),
                 ("W R", "Holds the lab to its charter and its safety rules, and fights the ministry for every budget."),
                 ("G", "Keeps a lab that serves the towns around it: the water tests, the weather, the open days.")],
       meets="need:competence+.1 need:autonomy+.05 res:money+.05 res:time-.15",
       ages=(40, 75), share=.000002,   # estimate: the directors of a country's national laboratories and research
                                       # institutes, a few dozen at a time, each for 5 to 10 years
       say="the director of a national laboratory",
       gained="appointed by the laboratory's board after years as a [research facility lead], [research group leader] or "
              "[celebrated inventor]",
       lost="the end of the term; a failed project; retirement",
       needs="[research facility lead], [research group leader] or [celebrated inventor] for years",
       turning="The lab's new system works, and the question is who gets to use it, and on whose terms."),
  dict(name="editor of a national paper", kind="career", sector="knowledge", institution="media", standing=3,
       sphere="gather", face="gather.U", ways="U R", refines="journalist",
       profiles=[("U R", "Chases the story the powerful want buried, and prints it when it is true."),
                 ("W B", "Runs the paper as an institution: its standards, its lawyers, its readers and its money."),
                 ("G", "Keeps the paper close to the towns it serves, and gives their voices the front page.")],
       meets="need:meaning+.1 need:autonomy+.05 res:ties+.05 res:time-.15 res:freedom-.05",
       ages=(35, 75), share=.000002,   # estimate: the editors of a country's national papers and news services, a
                                       # few dozen at a time, each for 4 to 10 years
       say="the editor of a national paper",
       gained="appointed by the paper's owners after years as a [journalist], usually with a [source who trusts you] and a "
              "name for getting things right",
       lost="the owners' displeasure; a story that proved wrong; the end of the paper",
       needs="[journalist] for years; [source who trusts you] or [name in the field]",
       turning="The story is ready to run tonight, and one source's safety and one fact are still unchecked."),
]

# ---------------------------------------------------------------- B: Coalition Builder, Opportunity Patron
TITLES += [
  dict(name="head of a national industry body", kind="career", sector="industry", institution="employer", standing=3,
       sphere="prod", face="prod.B", ways="B U", refines="chief executive; founder of a firm; celebrated inventor",
       profiles=[("B U", "Speaks for the country's industry, and knows what each firm wants before it asks."),
                 ("R G", "Holds the firms and the workers' towns together when a plant closes or a new one opens."),
                 ("W", "Writes the industry's code and its standards, and makes the members keep them.")],
       meets="need:autonomy+.08 need:competence+.06 res:money+.08 res:time-.15 res:ties+.03",
       ages=(40, 80), share=.000005,   # estimate: the heads of a country's national employers' federations, trade
                                       # associations and chambers, about a hundred at a time, each for 4 to 8 years
       say="the head of a national industry body",
       gained="elected by the industry's members after years as a [chief executive], [founder of a firm] or [celebrated "
              "inventor], usually with [a seat on boards]",
       lost="the members' vote; a split in the industry; retirement",
       needs="[chief executive], [founder of a firm] or [celebrated inventor] for years; [a seat on boards] or "
             "[investors who back you]",
       turning="Bringing in the rival firms would double the body's weight, and they would change what it stands for."),
  dict(name="head of a national bank or exchange", kind="career", sector="services", institution="bank", standing=3,
       sphere="comm", face="comm.B", ways="B U", refines="chief executive; accountant",
       profiles=[("B U", "Moves the country's money where the returns will be, and reads the markets before they turn."),
                 ("R G", "Backs the new firm nobody else would, and the town that needed it."),
                 ("W", "Keeps the rules of the exchange and the bank's word, so the whole country can trust its money.")],
       meets="need:safety+.05 need:autonomy+.08 res:money+.15 res:time-.15 res:freedom-.05",
       ages=(40, 80), share=.000001,   # estimate: a country's central bank governor and deputies, the chief executives
                                       # of its largest banks and the head of its exchange, about 20 at a time
       say="the head of a national bank or exchange",
       gained="appointed by the board or the government after years as a [chief executive] or an [accountant], with [investors who "
              "back you] or [a seat on boards]",
       lost="a crash; a vote of the board or the government; retirement",
       needs="[chief executive] for years, or an [accountant] of many years with [a seat on boards]",
       turning="One great bet could change the country's industry, and the same money could back fifty smaller ones."),
]

# ---------------------------------------------------------------- R: National Virtuoso
TITLES += [
  dict(name="celebrated star of stage or sport", kind="career", sector="services", institution="media", standing=3,
       sphere="arts", face="arts.R", ways="R B", refines="lead actor or actress; professional athlete; touring musician",
       profiles=[("R B", "Plays for the whole country, and the whole country watches: the nerve, the flair, the name."),
                 ("W G", "Carries the country's flag and its hopes, and goes home to the street that raised them."),
                 ("U", "Has studied every move and every line until the impossible looks easy.")],
       meets="need:autonomy+.08 need:meaning+.08 res:money+.1 res:time-.12 res:freedom-.12",
       ages=(18, 90), share=.00002,   # estimate: the actors, musicians and athletes whom most of a country knows by name
                                      # in a generation, a few hundred to a thousand
       say="a celebrated star of stage or sport",
       gained="a performance or a season the whole country watches, after years as a [lead actor or actress], [professional athlete] or "
              "[touring musician]",
       lost="never wholly; the fame fades when the work stops",
       needs="[lead actor or actress], [professional athlete] or [touring musician] for years; [a household name] "
             "often follows",
       turning="A strange, daring signature piece is ready, and a safe, well-paid offer is on the table."),
]

# ---------------------------------------------------------------- G: Living-Land Steward, Living-Heritage Keeper,
# ---------------------------------------------------------------- Community Weaver
TITLES += [
  dict(name="head of the national parks", kind="career", sector="public", institution="ministry", standing=3,
       sphere="prod", face="prod.G", ways="G U", refines="park ranger; forester",
       profiles=[("G U", "Knows every protected valley and what lives in it, and keeps the counts that prove it."),
                 ("W B", "Runs the parks as a public trust: the rules, the budgets, the farmers' and the councils' deals."),
                 ("R", "Stands in front of the diggers, and takes the fight for the wild to the capital.")],
       meets="need:meaning+.12 need:autonomy+.05 res:time-.15 res:health+.03",
       ages=(35, 75), share=.000001,   # estimate: the heads of a country's national park authorities and its parks
                                       # agency, about 15 at a time, each for 5 to 10 years
       say="the head of the national parks",
       gained="appointed by the government after years as a [park ranger] or [forester], often with a land kept well",
       lost="the end of the term; the government's displeasure; retirement",
       needs="[park ranger] or [forester] for years; the trust of the farmers and the walkers",
       turning="A protected valley could be closed to its farmers tomorrow, or saved more slowly with their agreement."),
  dict(name="keeper of the national heritage", kind="career", sector="public", institution="charity", standing=3,
       sphere="arts", face="arts.G", ways="G R", refines="museum curator; archivist; master craftsperson; folk musician",
       profiles=[("G R", "Keeps the old songs, crafts and places alive, and sings them louder than anyone."),
                 ("W B", "Runs the heritage trust's houses and collections, its members and its money."),
                 ("U", "Knows the record behind every object and every tune, and what is true in the old stories.")],
       meets="need:meaning+.12 need:belonging+.06 res:time-.12 res:ties+.05",
       ages=(40, 90), share=.000003,   # estimate: the heads of a country's national heritage trusts, museums, archives
                                       # and folk institutions, a few dozen at a time
       say="the keeper of the national heritage",
       gained="chosen by the heritage trust's council after years as a [museum curator], [archivist], [master craftsperson] "
              "or [folk musician]",
       lost="stepping down; a vote of the trust's council; retirement",
       needs="years as a [museum curator], [archivist], [master craftsperson] or [folk musician]",
       turning="The old ways can be kept exactly as they were, or changed so the young will take them up."),
  dict(name="head of a national charity", kind="community", institution="charity", standing=3, sphere="care",
       face="care.G", ways="G W", refines="community centre manager; community-garden coordinator; renowned healer",
       profiles=[("G W", "Holds hundreds of local groups together, and knows the people in each of them."),
                 ("U R", "Turns a campaign into a change in the law, and the evidence into an argument nobody can wave off."),
                 ("B", "Runs the charity like a great firm: the donors, the brand, the reach into every town.")],
       meets="need:meaning+.12 need:belonging+.06 res:time-.15 res:money-.03",
       ages=(35, 85), share=.00001,   # estimate: the chief executives and chairs of a country's large national
                                      # charities and federations of local groups, several hundred at a time
       say="the head of a national charity",
       gained="chosen by the trustees after years as a [community centre manager], a [community-garden "
              "coordinator] or a [renowned healer], with a [good name in town]",
       lost="stepping down; the trustees' vote; a scandal",
       needs="years leading a local group or a care service; [good name in town]",
       turning="One plan from the centre would help every branch, and the branches want to run themselves."),
]

# ---------------------------------------------------------------- the fifteen routes' assets
# One per route (Outer world's route data, chroma-world/spheres/data/world_fit.json "national" "routes": each route's
# asset and obligations), earned in the route's seat (roles.py) or by the Library's route encounters, and kept after
# the seat as the route's influence: a standing is a reputation that opens doors, a bond is people who answer, an asset
# is something held and kept running. Each colour's three routes hold one of each. Odds where the kind has them (.05,
# as the packs' other standings and bonds). The obligations are in lost: an asset is kept by keeping its obligation
# (decision #9's selective upkeep), and skill_half says how long a standing or bond lasts unused.
PERKS += [
  # W
  dict(name="a standing mandate", kind="standing", ways="W", odds=.05, skill_half=4, retires=None,
       ages=(30, 110), share=.0000005,   # with [head of government]
       say="holds a mandate from people who voted for the promise",
       gained="an election won on a promise, as the [head of government] or a [party leader] heading one",
       lost="the promise broken, or a compromise nobody was told about; it fades in the years after office",
       needs="[head of government] or [party leader]"),
  dict(name="a working public service", kind="asset", ways="W", odds=0, skill_half=None, retires=None,
       ages=(25, 110), share=.00001,   # estimate: ministers whose clinics, schools or help lines outlived their office
       say="built a public service people rely on",
       gained="years as a [minister] who carried a service through from the plan to every town",
       lost="kept only while it keeps running when budgets fall; a later government may close it, and the name stays",
       needs="[minister]"),
  dict(name="standing with both sides", kind="bond", ways="W", odds=.05, skill_half=10, retires=None,
       ages=(30, 110), share=.0001,   # estimate: mediators, faith heads and fixers whom both sides of a dispute trust
       say="is invited where others are shut out",
       gained="a split settled with neither side walking away, as a [mediator], a [head of a faith order] or the "
              "[head of a national faith body]",
       lost="taking one side in public; a settlement broken",
       needs="[mediator], [head of a faith order] or [head of a national faith body]"),
  # U
  dict(name="a finding and its method", kind="standing", ways="U", odds=.05, skill_half=20, retires=None,
       ages=(30, 110), share=.000005,   # estimate: scientists whose finding shaped a national decision
       say="made a finding the country relies on, and showed how",
       gained="advice as the [chief scientist], or [published research], that held up when it was tested",
       lost="a result found wrong and not corrected in public; a result corrected keeps it",
       needs="[chief scientist] or [published research]"),
  dict(name="a working national system", kind="asset", ways="U", odds=0, skill_half=None, retires=None,
       ages=(30, 110), share=.000002,   # estimate: the designers of a country's grids, networks and standards
       say="designed a system the country runs on",
       gained="a machine, a method or a network built at a national laboratory and taken up across the country",
       lost="kept only while it is kept safe and maintained as it spreads; a newer system may replace it",
       needs="[director of a national laboratory] or [celebrated inventor]"),
  dict(name="a record and its sources", kind="bond", ways="U", odds=.05, skill_half=4, retires=None,
       ages=(25, 110), share=.00002,   # estimate: editors and reporters with sources in every part of public life
       say="has a record that stands and the sources behind it",
       gained="years as the [editor of a national paper] or a [journalist] who protected every source and printed "
              "only what was checked",
       lost="a source exposed; a story printed that was not true; years away from the news",
       needs="[editor of a national paper] or [journalist]"),
  # B
  dict(name="the voice of a whole industry", kind="standing", ways="B", odds=.05, skill_half=6, retires=None,
       ages=(35, 110), share=.000005,   # estimate: the leaders who held an industry's rival firms together
       say="speaks for a whole industry, and the members move on cue",
       gained="years as the [head of a national industry body] that brought the rivals in",
       lost="failing one of the groups that moved together, until it leaves; years out of the industry",
       needs="[head of a national industry body]"),
  dict(name="a firm and its people", kind="bond", ways="B", odds=.05, skill_half=10, retires=None,
       ages=(30, 110), share=.00005,   # with [magnate]
       say="has a firm whose people stand by them",
       gained="years as a [magnate] who kept the firm standing and its people paid through bad years",
       lost="a firm broken up, or its people let go to save the owner",
       needs="[magnate] or [chief executive]"),
  dict(name="a portfolio of people backed", kind="asset", ways="B", odds=0, skill_half=None, retires=None,
       ages=(35, 110), share=.000005,   # estimate: bankers and investors who backed many ventures of their own choosing
       say="has backed a portfolio of people and their ventures",
       gained="ventures backed as the [head of a national bank or exchange], or with [investors who back you]",
       lost="abandoning those backed when they fail; a crash",
       needs="[head of a national bank or exchange] or [investors who back you]"),
  # R
  dict(name="a following that turns out", kind="standing", ways="R", odds=.05, skill_half=5, retires=None,
       ages=(25, 110), share=.00001,   # estimate: leaders who can bring their followers onto the streets
       say="has a following that turns out when called",
       gained="years as a [party leader], or a leader with [a following in the party], who took the cause to the "
              "streets",
       lost="a betrayal of those who turned out; years out of the fight",
       needs="[party leader] or [a following in the party]"),
  dict(name="a unit that trusts its leader", kind="bond", ways="R", odds=.05, skill_half=8, retires=None,
       ages=(30, 110), share=.00003,   # with [general]
       say="leads soldiers who trust them",
       gained="years as a [general] or an [army officer] who brought the soldiers home and answered for every order",
       lost="an order that cost lives for nothing; years out of uniform",
       needs="[general] or [army officer]"),
  dict(name="a signature work and its audience", kind="asset", ways="R", odds=0, skill_half=None, retires=None,
       ages=(18, 110), share=.00002,   # with [celebrated star of stage or sport]
       say="has a signature work and an audience that waits for the next",
       gained="the daring signature piece, made as a [celebrated star of stage or sport]",
       lost="kept while the work stays honest; it fades from view when the work stops, and the work stays",
       needs="[celebrated star of stage or sport]"),
  # G
  dict(name="a living tradition kept", kind="standing", ways="G", odds=.05, skill_half=20, retires=None,
       ages=(30, 110), share=.000005,   # estimate: the keepers whose name the country's old crafts and songs carry
       say="keeps a living tradition: its songs, crafts, rites and places",
       gained="years as the [keeper of the national heritage], or a lifetime as a [master craftsperson] or [folk "
              "musician] who passed the old ways on",
       lost="it fades when no one learns the old ways from them",
       needs="[keeper of the national heritage], [master craftsperson] or [folk musician]"),
  dict(name="a web of groups that help each other", kind="bond", ways="G", odds=.05, skill_half=6, retires=None,
       ages=(30, 110), share=.00002,   # estimate: the leaders of networks of local groups across a country
       say="holds a web of groups together that help each other",
       gained="years as the [head of a national charity] who kept each branch its own while they acted together",
       lost="the branches taken over from the centre, or left to drift apart",
       needs="[head of a national charity] or [community centre manager]"),
  dict(name="a stretch of land kept alive", kind="asset", ways="G", odds=0, skill_half=None, retires=None,
       ages=(30, 110), share=.000005,   # estimate: the people who won lasting care for a park, a reserve or a coast
       say="kept a stretch of land alive, with the people who keep it",
       gained="a valley, a coast or a forest kept by the [head of the national parks], a [park ranger] or a [forester] "
              "working with its farmers",
       lost="the protection lifted by a later government; the keepers gone",
       needs="[head of the national parks], [park ranger] or [forester]"),
]
