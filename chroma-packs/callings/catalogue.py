# Chroma content pack: The Five Callings (faith, invention, business, command and healing; modern Earth, with the
# tribal and magic worlds). Catalogue: titles and perks. Pathways and packs thread, 2026-10-19, for v24 (plan
# chroma-ideas/next-table-2026-10-19/plan.md, section 5: "Then the missing faces that keep each colour pair fair"). The
# four packs' public callings cover every colour pair twice and no single colour (chroma-packs/notes/
# v24-aims-ladders.md); the Vision thread agreed on 10-19 (12:04 UTC) to fill the five singles now: W the faith leader,
# U the inventor, B the magnate, R the commander, G the healer. The steward of the land joins with the nature sphere
# (v25). Plain data in the fields of chroma-library/earth_perks_titles.py (its header defines every field); nothing is
# imported and nothing runs. Modern Earth terms, as the base catalogue; the forms of every title and perk in the tribal
# and magic worlds are in worlds.py next to this file.
#
# SWITCHED OFF: `callings` is not in batch.PACKS, so nothing reads this folder and no life changes until the Engine adds
# it, with Emren's word.
#
# The pack only adds. Each road climbs from base titles: the faith leader from [ordained religious minister] or [member
# of a monastic community], the inventor from [software developer], [civil engineer], [machinist], [electrician] or
# [founder of a firm], the magnate from [shop owner], [founder of a firm], [café or bar owner] or [shift manager], the
# commander from [soldier] (or [graduate] and the academy), the healer from [nurse] or [midwife]. It reuses [scripture],
# [leading a ceremony], [fixing things], [workshop], [tools of one's own], [striking a deal], [selling], [bookkeeping],
# [shares], [rank], [old comrades], [award for bravery], [keeping fit], [home nursing], [emergency care],
# [professional registration], [good name in town], [name in the field], the shared reach ladder ([known across the
# country], [a household name]: core/reach.py) and the Historic marker ([a work that outlives you]: core/legacy.py).
#
# Choices, on purpose (PACK.md, "Departures"):
#   - Each road adds two titles: the Known rung ([senior cleric], [inventor], [chief executive], [army officer],
#     [senior nurse or midwife]) and the summit. Four summits are facets (the engine's refines), as [renowned artist]:
#     a celebrated inventor keeps inventing, a magnate keeps running the firm, a general is still an officer, a
#     renowned healer keeps healing. [head of a faith order] refines [senior cleric] and [member of a monastic
#     community], so the head of a house of monks or nuns can rise without a parish.
#   - The faith titles are of the faith kind, as the base [ordained religious minister]: a calling of faith is a
#     commitment of faith, not a career.
#   - Colour balance: every title has three profiles, the road's single colour and two pairs that cover the other four,
#     so the titles are exactly even (W U B R G 6.00 each). Every perk kind holds three perks (one single colour and
#     two pairs covering the other four), and each colour is the single of one kind, so the perks are exactly even and
#     every kind holds all five colours. Each road leans to its colour through its ways and its moments, never as a
#     wall: every colour can hold every title.
#
# Shares: share of people in a modern rich country who ever hold it. Sources: US Bureau of Labor Statistics (May 2023:
# about 200,000 employed chief executives); the US Department of Defense's active-duty figures (about 1 member in 6 is
# an officer; under 1,000 generals and admirals at a time); Bell, Chetty, Jaravel, Petkova and Van Reenen, "Who Becomes
# an Inventor in America?" (2019: about 1.6 in 1,000 people born in 1980 held a patent by their thirties); the NHS
# workforce statistics (about 1 registered nurse or midwife in 8 is at band 7 or above: ward managers, charge nurses,
# lead midwives). Everything else is an estimate, and says so. Real names stay in these comments: the moments never name
# a real person, faith, order, firm, army, war, country, hospital or school.
#
# The outer world's keywords (chroma-engine/world-fields.md, W38 and W40): sector=, institution= (an at: value) and
# standing= (0 an ordinary person, 1 local, 2 inside power, 3 national) on every career and summit. Spheres (item 15,
# Engine 10-09 21:51): sphere= and face= on every title.
TITLES = []
PERKS = []

# ---------------------------------------------------------------- W: the faith leader (sphere faith)
TITLES += [
  dict(name="senior cleric", kind="faith", sphere="faith", face="faith.W", ways="W",
       profiles=[("W", "Keeps the rule, the rites and the calendar of a great congregation, and the people in them."),
                 ("U B", "Runs many congregations as a well-ordered house, and knows where every coin and quarrel is."),
                 ("R G", "Preaches with fire to the poor and the young, and keeps the old feasts of field and season.")],
       meets="need:meaning+.12 need:belonging+.06 need:autonomy-.03 res:ties+.05 res:time-.12",
       ages=(35, 90), share=.0005,   # estimate: about 1 minister of religion in 8 comes to lead a great congregation
                                     # or to oversee others (the base [ordained religious minister] is .004)
       say="a senior cleric",
       gained="'the congregation needs a senior minister' after years as an [ordained religious minister] or a "
              "[member of a monastic community]",
       lost="retirement; a scandal; the faith's own leaders moving them on",
       needs="[ordained religious minister] or [member of a monastic community] for years; [leading a ceremony] and "
             "[scripture]; [a degree in theology] in most faiths"),
  dict(name="head of a faith order", kind="faith", sphere="faith", face="faith.W", ways="W",
       refines="senior cleric; member of a monastic community",
       profiles=[("W", "Leads a whole faith or order through its law, its councils and its long memory."),
                 ("U G", "Leads by learning and by stillness: the scholar of the scriptures, the mystic of the hills."),
                 ("B R", "Leads by force of person: the voice that fills the great square and the halls of power.")],
       meets="need:meaning+.12 need:autonomy+.05 res:ties+.05 res:time-.15 res:freedom-.08",
       ages=(45, 105), share=.00002,   # estimate: the heads of a country's faith bodies, religious orders and great
                                       # houses of monks or nuns
       say="at the head of a faith order",
       gained="'the order chooses its head', won by a [senior cleric] or a [member of a monastic community] of many "
              "years",
       lost="death in office (most serve for life); stepping down; a split in the faith",
       needs="[senior cleric] or [member of a monastic community] for many years; [a flock that follows you] or "
             "[known across the country] usually come first",
       turning="The council of the faith is divided, and every side waits to hear which way the head will lean."),
]

# ---------------------------------------------------------------- U: the inventor (sphere prod)
TITLES += [
  dict(name="inventor", kind="career", sector="services", institution="employer", standing=1, sphere="prod",
       face="prod.U", ways="U",
       profiles=[("U", "Sees how a thing could work, and will not stop until it does."),
                 ("W B", "Makes the safe, tested, patented version the world can buy, and owns it."),
                 ("R G", "Tinkers in the shed with whatever is to hand, and mends old machines into new ones.")],
       meets="need:autonomy+.1 need:competence+.1 need:safety-.05 res:money+.03 res:time-.12",
       ages=(18, 90), share=.0005,   # Bell et al. (2019): about 1.6 in 1,000 hold a patent by their thirties; about a
                                     # third of them make a living from their own inventions for years (estimate)
       say="an inventor",
       gained="'the prototype works' after years as a [software developer], [civil engineer], [machinist], "
              "[electrician] or [founder of a firm]",
       lost="the invention not selling; a bigger firm's copy; a steady job in its place",
       needs="years at a technical trade, or [fixing things] and a [workshop]; [prototyping] usually comes first"),
  dict(name="celebrated inventor", kind="career", institution="media", standing=2, sphere="prod", face="prod.U",
       ways="U", refines="inventor",
       profiles=[("U", "Made the thing everyone now uses, and the name is in the schoolbooks."),
                 ("W G", "Made something that keeps people safe, fed or well, and gave much of it away."),
                 ("B R", "Made a fortune from a daring idea, and the rivals who laughed now copy it.")],
       meets="need:meaning+.1 need:autonomy+.05 res:money+.08 res:time-.05",
       ages=(25, 100), share=.00005,   # estimate: inventors whose invention most households know by name
       say="a celebrated inventor",
       gained="'an invention in every home' after years as an [inventor]",
       lost="never; newer inventions outshine it, and the name stays",
       needs="[inventor] for years; [a patent of your own] and [an invention in everyday use] usually come first"),
]

# ---------------------------------------------------------------- B: the magnate (sphere comm)
TITLES += [
  dict(name="chief executive", kind="career", sector="services", institution="employer", standing=2, sphere="comm",
       face="comm.B", ways="B",
       profiles=[("B", "Runs a large firm to win: the numbers, the rivals, the next deal."),
                 ("W U", "Runs the firm as a sound institution: clear rules, honest books, a plan for ten years."),
                 ("R G", "Runs the firm like a family or a crusade: workers known by name, risks taken for a cause.")],
       meets="need:autonomy+.08 need:competence+.08 res:money+.12 res:time-.15 res:ties-.05",
       ages=(28, 85), share=.002,   # BLS May 2023: about 200,000 chief executives employed; with those of smaller
                                    # firms and the years each holds it, about 2 lives in 1,000 (estimate)
       say="the chief executive of a firm",
       gained="'the board needs a chief executive' after years as a [founder of a firm], a [shop owner], a [café or "
              "bar owner] or a [shift manager]",
       lost="the board's vote; a takeover; retirement",
       needs="a firm of one's own or years in management; [striking a deal] or [bookkeeping]"),
  dict(name="magnate", kind="career", institution="employer", standing=3, sphere="comm", face="comm.B", ways="B",
       refines="chief executive; founder of a firm",
       profiles=[("B", "Owns a business empire, and the country's markets move when it moves."),
                 ("W G", "Builds a great family firm over decades, and keeps faith with its workers and its town."),
                 ("U R", "Builds an empire fast, by a system nobody else saw and a risk nobody else would take.")],
       meets="need:autonomy+.1 need:safety+.05 res:money+.15 res:time-.12 res:ties-.05",
       ages=(30, 100), share=.00005,   # estimate: owners of a country's great business groups (fewer than 1 in 100,000
                                       # are billionaires; the national tier below them is a few times larger)
       say="a magnate",
       gained="'a rival firm is for sale', won by a [chief executive] or [founder of a firm] of years with "
              "[investors who back you] or [shares]",
       lost="ruin; a takeover; the empire handed on",
       needs="[chief executive] or [founder of a firm] for years; [a business empire] follows",
       turning="Thousands of jobs and the town's biggest employer hang on one signature, and it is theirs."),
]

# ---------------------------------------------------------------- R: the commander (sphere prot)
TITLES += [
  dict(name="army officer", kind="career", sector="public", institution="army", standing=1, sphere="prot",
       face="prot.R", ways="R",
       profiles=[("R", "Leads from the front: first out, last back, and the soldiers know it."),
                 ("W U", "Leads by the book and the map: orders clear, supplies counted, the plan thought through."),
                 ("B G", "Leads for the unit: ambitious for it, fierce for it, a family that comes home together.")],
       meets="need:belonging+.08 need:meaning+.06 need:autonomy-.05 res:money+.05 res:freedom-.12 res:health-.05",
       ages=(20, 60), share=.006,   # US Department of Defense: about 1 in 6 on active duty is an officer; with the
                                    # base [soldier] at .05 and the reserves, about 6 lives in 1,000 (estimate)
       say="an army officer",
       gained="'officer selection' after years as a [soldier], or the academy after school or a degree ([graduate], "
              "[national service done])",
       lost="the end of a commission; an injury; a court-martial; retirement",
       needs="[soldier] for years, or [graduate] and the academy; [keeping fit]; no serious record"),
  dict(name="general", kind="career", institution="army", standing=3, sphere="prot", face="prot.R", ways="R",
       refines="army officer",
       profiles=[("R", "Commands by courage and will, and the soldiers would follow anywhere."),
                 ("W B", "Commands through rank and law: the chain of command, the code, the minister's ear."),
                 ("U G", "Commands by foresight and care: supply, patience, and soldiers kept alive.")],
       meets="need:meaning+.1 need:autonomy+.05 res:money+.05 res:time-.15 res:freedom-.1",
       ages=(40, 70), share=.00003,   # US DoD: under 1,000 generals and admirals at a time among about 1.3 million on
                                      # active duty; over all lives, about 3 in 100,000 (estimate)
       say="a general",
       gained="'the army needs a new general', won by an [army officer] of many years",
       lost="retirement; a defeat; the government's displeasure",
       needs="[army officer] for many years; [rank]; [mentioned in dispatches] or [award for bravery] often",
       turning="The government wants the soldiers somewhere they should not go, and the order would be the general's."),
]

# ---------------------------------------------------------------- G: the healer (sphere care)
TITLES += [
  dict(name="senior nurse or midwife", kind="career", sector="public", institution="hospital", standing=1,
       sphere="care", face="care.G", ways="G",
       profiles=[("G", "Knows every family on the ward and the district, from the first breath to the last."),
                 ("W U", "Runs the ward or the birth centre by the protocol, and teaches the young ones why it matters."),
                 ("B R", "Fights the managers for beds and staff, and goes in first when the night goes wrong.")],
       meets="need:meaning+.12 need:belonging+.06 res:money+.05 res:time-.12 res:health-.05",
       ages=(26, 70), share=.004,   # NHS workforce statistics: about 1 registered nurse or midwife in 8 reaches band 7
                                    # or above (ward manager, charge nurse, lead midwife); the base [nurse] is .03
       say="a senior nurse or midwife",
       gained="'the ward needs someone in charge' after years as a [nurse] or a [midwife]",
       lost="retirement; burnout; a move into management or teaching",
       needs="[nurse] or [midwife] for years; [professional registration]"),
  dict(name="renowned healer", kind="career", institution="hospital", standing=2, sphere="care", face="care.G",
       ways="G", refines="senior nurse or midwife; nurse; midwife; physician; complementary therapist",
       profiles=[("G", "Heals with patience and touch, and families travel far to be in their hands."),
                 ("W R", "Heals where it is hardest: the flooded valley, the epidemic ward, the night nobody will work."),
                 ("U B", "Heals by a skill nobody else has, and the name draws patients and pupils from everywhere.")],
       meets="need:meaning+.12 need:belonging+.05 res:ties+.05 res:time-.1",
       ages=(30, 100), share=.00005,   # estimate: healers whose name is known across the country for their care, a
                                       # way of caring they began, or a place of healing they founded
       say="a healer known across the land",
       gained="'patients come from far away' after years as a [senior nurse or midwife], [midwife], [nurse], "
              "[physician] or [complementary therapist]",
       lost="never; the name stays in the families",
       needs="years of healing; [families who send for you] usually come first"),
]

# ---------------------------------------------------------------- perks: skills (single R)
PERKS += [
  dict(name="leading soldiers", kind="skill", ways="R", odds=.05, skill_half=12, retires=None,
       ages=(18, 75), share=.008,   # estimate: officers, sergeants and corporals who led a section or more
       say="can lead soldiers",
       gained="years as a [soldier] or [army officer]; 'the corporal is hurt on exercise'",
       lost="years out of uniform",
       needs="[soldier] or [army officer]"),
  dict(name="preaching", kind="skill", ways="W G", odds=.05, skill_half=15, retires=None,
       ages=(16, 100), share=.006,   # estimate: ministers, lay preachers and street preachers
       say="can preach",
       gained="years as an [ordained religious minister], [lay religious teacher] or [street preacher]; [scripture] "
              "and [public speaking]",
       lost="years without a pulpit",
       needs="[scripture]"),
  dict(name="prototyping", kind="skill", ways="U B", odds=.05, skill_half=10, retires=None,
       ages=(12, 95), share=.01,   # estimate: people who build working models of their own designs
       say="builds prototypes",
       gained="'the idea in the shed at night'; years as a [machinist], [electrician], [software developer] or "
              "[civil engineer]; a [workshop]",
       lost="years without building anything",
       needs="[fixing things], [machining] or [writing code]"),
]

# ---------------------------------------------------------------- perks: credentials (single W)
PERKS += [
  dict(name="a degree in theology", kind="credential", ways="W", odds=0, skill_half=None, retires=None,
       ages=(21, 100), share=.003,   # estimate: most ministers of religion and some lay teachers
       say="has a degree in theology",
       gained="years at a seminary, a faith's college or a university, often before ordination",
       lost="never",
       needs="[graduate] or a faith's own college; [scripture]"),
  dict(name="an officer's commission", kind="credential", ways="R B", odds=0, skill_half=None, retires=None,
       ages=(20, 100), share=.006,   # with [army officer]
       say="holds a commission",
       gained="'officer selection' and the academy",
       lost="resigning the commission; a court-martial",
       needs="[soldier] for years, or [graduate]"),
  dict(name="licence to prescribe", kind="credential", ways="G U", odds=0, skill_half=None, retires=None,
       ages=(24, 100), share=.006,   # estimate: nurses and midwives with the extra prescribing course, and
                                     # physicians
       say="can prescribe",
       gained="a prescribing course after years as a [nurse] or [midwife]; a [physician]'s registration",
       lost="losing registration",
       needs="[professional registration]"),
]

# ---------------------------------------------------------------- perks: standing (single U)
PERKS += [
  dict(name="an invention in everyday use", kind="standing", ways="U", odds=.05, skill_half=30, retires=None,
       ages=(20, 110), share=.0002,   # estimate: inventors of something sold in the shops or built into everyday things
       say="made something people use every day",
       gained="'the prototype works', then a firm that makes it, or 'an invention in every home'",
       lost="something better replacing it; the name stays",
       needs="[inventor] or [a patent of your own]"),
  dict(name="a seat on boards", kind="standing", ways="B W", odds=.05, skill_half=10, retires=None,
       ages=(30, 95), share=.002,   # estimate: directors of firms, charities and public bodies
       say="sits on boards",
       gained="years as a [chief executive], [founder of a firm] or [magnate]; [investors who back you]",
       lost="retiring from the boards; a scandal",
       needs="a firm run for years"),
  dict(name="mentioned in dispatches", kind="standing", ways="R G", odds=.04, skill_half=25, retires=None,
       ages=(18, 110), share=.002,   # estimate: soldiers whose courage or care was named in a report from the field
       say="was mentioned in dispatches",
       gained="'the corporal is hurt on exercise', a night that went right, years on [leading soldiers]",
       lost="never",
       needs="[soldier] or [army officer]"),
]

# ---------------------------------------------------------------- perks: bonds (single G)
PERKS += [
  dict(name="families who send for you", kind="bond", ways="G", odds=.05, skill_half=15, retires=None,
       ages=(22, 100), share=.005,   # estimate: nurses, midwives and doctors whom a district's families ask for by name
       say="the families send for them",
       gained="'the birth that will not wait', 'a family asks you to stay to the end', years on a district or ward",
       lost="years away from the district",
       needs="[nurse], [midwife], [physician], [care worker] or [senior nurse or midwife]"),
  dict(name="a flock that follows you", kind="bond", ways="W R", odds=.05, skill_half=12, retires=None,
       ages=(25, 100), share=.002,   # estimate: ministers whose congregation would follow them to another place
       say="has a flock that follows them",
       gained="'the parish no one else will take', [preaching] kept up for years",
       lost="years away from a pulpit; a scandal",
       needs="[ordained religious minister], [street preacher] or [senior cleric]"),
  dict(name="investors who back you", kind="bond", ways="B U", odds=.05, skill_half=10, retires=None,
       ages=(20, 100), share=.003,   # estimate: founders and chief executives with backers who come back
       say="has investors behind them",
       gained="'a rival opens across the street', a first firm sold well, [striking a deal]",
       lost="a loss that burns them; years out of business",
       needs="[founder of a firm], [shop owner] or [chief executive]"),
]

# ---------------------------------------------------------------- perks: assets (single B)
PERKS += [
  dict(name="a business empire", kind="asset", ways="B", odds=0, skill_half=None, retires=None,
       ages=(30, 110), share=.00005,   # with [magnate]
       say="owns a business empire",
       gained="'a rival firm is for sale', firms bought one by one over years",
       lost="ruin; selling up; handing it on",
       needs="[magnate]"),
  dict(name="a patent of your own", kind="asset", ways="U R", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.002,   # Bell et al. (2019): about 1.6 in 1,000 hold a patent by their thirties
       say="holds a patent",
       gained="'the prototype works', and the fees and forms for a patent",
       lost="the patent running out after twenty years; selling it",
       needs="[prototyping]; [savings] or a firm to pay the fees"),
  dict(name="a clinic of your own", kind="asset", ways="G W", odds=0, skill_half=None, retires=None,
       ages=(28, 100), share=.0005,   # estimate: a practice, birth centre, clinic or hospice founded or led for years
       say="runs a clinic of their own",
       gained="'the managers want the birth centre closed', years as a [senior nurse or midwife], [physician] or "
              "[renowned healer]",
       lost="the money running out; handing it on",
       needs="[senior nurse or midwife], [physician] or [renowned healer]; [savings] or backers"),
]
