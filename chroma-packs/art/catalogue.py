# Chroma content pack: Art and Writing (modern Earth, with the tribal and magic worlds). Catalogue: titles and perks.
# Pathways and packs thread, 2026-10-10, for v22.4 (coordinator relay 17:10 UTC: "Go with your recommendation for
# v22.4... build the three green entry jobs and the Art and Writing slice now as PRs, held"). Emren asked on 10-10 that
# red-led choices lead to artist, and that each life see richer lanes at different depths
# (chroma-packs/notes/v22.4-lanes-sizing.md, finding 2). This is a slice of the planned pack
# (chroma-pack-ideas/next-packs.md, "Art and Writing"): visual art and writing; music stays with a later pack. Plain
# data in the fields of chroma-library/earth_perks_titles.py (its header defines every field); nothing is imported and
# nothing runs. Modern Earth terms, as the base catalogue; the forms of every title and perk in the tribal and magic
# worlds are in worlds.py next to this file.
#
# The pack only adds. It reuses the base catalogue's [novelist] (the writing road's career rung), [craft maker] (the
# green road's first rung), [teacher], [book editor], [museum curator], [shop owner], [drawing and painting], [writing
# stories], [book in print], [studio of one's own], [workshop], [tools of one's own], [mentor], [patron], [selling],
# [striking a deal], [teaching], [graduate], [scholarship], [savings], [following online], [name on the local scene],
# [good name in town], [contact in the trade], [public speaking] and [cleared to work with children], and the shared
# reach ladder ([known across the country], [a household name]: core/reach.py) instead of repeating them.
#
# Choices, on purpose (PACK.md, "Departures"):
#   - The two summits are facets (the engine's refines), like [lead actor or actress]: a renowned artist keeps painting
#     and a celebrated author keeps writing. [renowned artist] sits on any of the four visual careers; [celebrated
#     author] on the base [novelist], which stands for every writer of books, poems included.
#   - The taste rung is two community titles held beside a day job ([open-mic poet], [life-drawing regular]), as nearly
#     everyone who writes or draws does.
#   - [art school student] is a status: a three-year course.
#   - No child holds a career title: a child draws and writes through the base skills and the school's own moments.
#   - Colour balance: every title with colours has three profiles, one single colour and two pairs that cover the
#     other four, and each colour is the single colour of two titles, so the titles are exactly even. Every perk kind
#     holds three perks (one single colour and two pairs covering the other four), and each colour is the single of one
#     kind, so the perks are exactly even and every kind holds all five colours. Red is deepest through the roads, not
#     through the counts: the red road has four depths (taste, practice, profession, summit).
#
# Shares: share of people in a modern rich country who ever hold it. Sources: US Bureau of Labor Statistics (May 2023:
# about 30,000 employed fine artists, including painters, sculptors and illustrators, and about 260,000 graphic
# designers; most fine artists are self-employed and not in that count), the UK's higher-education statistics (creative
# arts and design is about 1 student in 12), Arts Council England's surveys (visual artists' median income from their
# practice well under a living wage), and the UK and US teaching workforce counts (about 1 secondary teacher in 25
# teaches art and design). Everything else is an estimate, and says so. Real names stay in these comments: the moments
# never name a real person, gallery, museum, prize, publisher or school.
#
# The outer world's keywords (chroma-engine/world-fields.md, W38 and W40): sector= on every career, institution= (an at:
# value) and standing= (0 an ordinary person, 1 local, 2 inside power, 3 national) on every career and summit. Spheres
# (item 15, Engine 10-09 21:51): sphere= and face= on careers and community titles; statuses are never tagged.
TITLES = []
PERKS = []

# ---------------------------------------------------------------- community: the taste rung
TITLES += [
  dict(name="open-mic poet", kind="community", sphere="arts", face="arts.R", ways="R B",
       profiles=[("R B", "Stands up with a page that shakes and reads the thing they could not say any other way."),
                 ("U", "Counts the syllables, redrafts all week and brings the poem back when it finally works."),
                 ("W G", "Reads the town's own stories at the library and the care home, where everyone knows them.")],
       meets="need:meaning+.08 need:belonging+.05 res:time-.03",
       ages=(15, 90), share=.01,   # estimate: most towns have a poetry or spoken-word night; about 1 life in 100
                                   # reads at one again and again for a year or more
       say="an open-mic poet",
       gained="'the poetry night at the back of the pub', a notebook kept since school ([writing poems]), a friend "
              "who drags them along to read",
       lost="no time any more, the night closing, a move away; the notebooks stay",
       needs="age 15 or more; something written to read"),
  dict(name="life-drawing regular", kind="community", sphere="arts", face="arts.U", ways="R U",
       profiles=[("R U", "Draws fast and badly and then well, chasing the line that says what the body says."),
                 ("G", "Draws the body as it is, old and heavy and alive, slowly and with something like love."),
                 ("W B", "Never misses the Tuesday class, keeps its quiet rules and means to get good enough to sell.")],
       meets="need:competence+.05 need:belonging+.03 res:time-.03",
       ages=(16, 95), share=.015,   # estimate: evening life classes, art societies and adult education
       say="a life-drawing regular",
       gained="'the evening class at the college', [drawing and painting] kept up since school, an art society's "
              "weekly session",
       lost="no time any more, the class closing, eyes or hands failing",
       needs="age 16 or more; a class nearby"),
]

# ---------------------------------------------------------------- careers: the practice rung (entry careers)
TITLES += [
  dict(name="street artist", kind="career", sector="services", institution="council", standing=0, sphere="arts",
       face="arts.R", ways="R G",
       profiles=[("R G", "Paints the walls of their own streets, big and fast, for the people who walk past them."),
                 ("W", "Plans the mural with the neighbours and the council, squares it up and paints it to last."),
                 ("U B", "Works anonymously and cleverly, and lets the name spread before the face does.")],
       meets="need:autonomy+.1 need:meaning+.05 res:money-.02 res:time-.08 need:safety-.03",
       ages=(16, 60), share=.0005,   # estimate: those who are paid for murals, shutters and walls for a year or more;
                                     # many more paint walls unpaid
       say="a street artist",
       gained="years of [drawing and painting] and walls painted for nothing, then 'a wall that needs a mural' and a "
              "first paid commission from a shop, a school or the council",
       lost="the commissions drying up, a fine or a bad fall, a steadier job, growing out of it",
       needs="[drawing and painting]; walls painted before, paid or not"),
  dict(name="illustrator for hire", kind="career", sector="knowledge", institution="media", standing=0,
       sphere="arts", face="arts.U", ways="U R",
       profiles=[("U R", "Finds a new way to draw every brief, and draws all night when the idea arrives."),
                 ("B", "Builds a style people pay for, a client list and a rate that goes up every year."),
                 ("W G", "Draws children's books and field guides, careful and kind, true to the thing drawn.")],
       meets="need:competence+.08 need:autonomy+.08 res:money+.02 res:time-.08 need:safety-.03",
       ages=(18, 80), share=.003,   # estimate: freelance illustrators for books, magazines, packaging and games; the
                                    # BLS counts only the employed ones
       say="an illustrator",
       gained="[art school student] or years of [drawing and painting], a portfolio, and 'the first commission' from "
              "a magazine, a publisher or a small firm",
       lost="the work drying up, a machine that draws cheaper, a steady job in design, eyes or hands failing",
       needs="[illustration] or [drawing and painting]; a portfolio"),
]

# ---------------------------------------------------------------- careers: the profession and the side roads
TITLES += [
  dict(name="painter or sculptor", kind="career", sector="services", institution="employer", standing=0,
       sphere="arts", face="arts.R", ways="R",
       profiles=[("R", "Makes the work they have to make, whatever it costs, and it shows."),
                 ("U W", "Studies the masters and the method, and builds each piece with patience and rigour."),
                 ("B G", "Works the clay, the stone and the body's decay, and will be known for it.")],
       meets="need:meaning+.1 need:autonomy+.1 need:safety-.05 res:money-.02 res:time-.1",
       ages=(20, 95), share=.001,   # estimate: those who earn a real part of their living from their own painting or
                                    # sculpture for some years; the BLS counts about 30,000 employed fine artists
       say="a painter",
       gained="[art school student] or long years as a [life-drawing regular], [street artist] or [illustrator for "
              "hire], then 'the first show' and work that sells",
       lost="the work not selling, a studio lost, another job taking over; the work remains",
       needs="[drawing and painting] or [sculpting]; years of practice; a place to work ([studio of one's own] helps)",
       turning="A gallery offers a show if the new work looks like the old work that sold."),
  dict(name="art teacher", kind="career", sector="knowledge", institution="school", standing=0, sphere="arts",
       face="arts.W", ways="W",
       profiles=[("W", "Keeps the art room open at lunch and teaches every child that drawing can be learned."),
                 ("U G", "Teaches the method and lets each child grow at their own pace, like a garden."),
                 ("B R", "Was an artist first, pushes the gifted ones hard and still paints at night.")],
       meets="need:meaning+.1 need:belonging+.05 res:money+.05 res:time-.1 res:health-.02",
       ages=(22, 70), share=.003,   # about 1 secondary teacher in 25 teaches art and design (UK and US workforce
                                    # counts); with turnover, about 3 lives in 1,000 (estimate)
       say="an art teacher",
       gained="[art school degree] and a teaching qualification, or a [teacher] who takes over the art room",
       lost="burnout, the art room cut from the timetable, retirement, a move into their own practice",
       needs="[art school degree] or [drawing and painting]; [graduate] and [professional registration]; [cleared to "
             "work with children]"),
  dict(name="gallery owner", kind="career", sector="services", institution="employer", standing=1, sphere="arts",
       face="arts.B", ways="B",
       profiles=[("B", "Picks the artists who will sell, and makes their names and their prices together."),
                 ("W U", "Hangs a careful, scholarly show and keeps honest books for every artist."),
                 ("R G", "Opens a room on the high street for the town's own makers, with wine on Friday nights.")],
       meets="need:autonomy+.08 need:competence+.05 res:money+.05 res:time-.12 need:safety-.05",
       ages=(25, 85), share=.0003,   # estimate: small commercial galleries are a few in each town and city
       say="a gallery owner",
       gained="years as a [painter or sculptor], an [art teacher], a [shop owner] or a [museum curator], [savings] "
              "and 'an empty shop on the corner'",
       lost="the rent rising, a bad season of sales, a partner leaving, selling up",
       needs="[savings] or a [patron]; an eye trained by years in the trade"),
  dict(name="master craftsperson", kind="career", sector="industry", institution="employer", standing=1,
       sphere="arts", face="arts.G", ways="G",
       profiles=[("G", "Makes it the old way, by hand, from the wood and clay of the place, for a lifetime."),
                 ("W U", "Holds the guild's standard and teaches it, every joint and glaze exactly right."),
                 ("B R", "Has a name and prices to match, and makes pieces people queue for.")],
       meets="need:competence+.1 need:autonomy+.08 need:meaning+.05 res:money+.02 res:time-.08",
       ages=(30, 95), share=.0008,   # estimate: potters, weavers, woodworkers, silversmiths and glassmakers whose work
                                     # is shown, collected or taught; many more make and sell beside another job
       say="a master craftsperson",
       gained="years as a [craft maker] or a [carpenter], [a maker's hallmark], a waiting list and an apprentice of "
              "their own",
       lost="hands or eyes failing, the workshop closing, retirement; the pieces outlive the maker",
       needs="[craft maker] or [carpenter] for years; [workshop] or [tools of one's own]"),
]

# ---------------------------------------------------------------- summits: facets on the career held
TITLES += [
  dict(name="renowned artist", kind="career", institution="media", standing=2, sphere="arts", face="arts.R",
       ways="R",
       profiles=[("R", "Made work so alive that it hangs where the whole country can see it."),
                 ("U B", "Played the art world's game well, and the ideas behind the work are argued over."),
                 ("W G", "Made the work that belongs to a people and a place, and is shown to their children.")],
       meets="need:meaning+.1 need:autonomy+.05 res:money+.05 res:time-.05",
       ages=(25, 100), share=.0001,   # estimate: artists with work in a national collection or a retrospective in a
                                      # national gallery
       say="a renowned artist",
       gained="'a work in the national collection' after years as a [painter or sculptor], [street artist], "
              "[illustrator for hire] or [master craftsperson]",
       lost="fashion moving on; the work stays in the collection",
       needs="a career in the visual arts for years; [a name in the art world], a [patron] or [works in collectors' "
             "hands] usually come first"),
  dict(name="celebrated author", kind="career", institution="media", standing=2, sphere="arts", face="arts.W",
       ways="R W",
       profiles=[("R W", "Wrote the book that says what a generation felt, in a form that will last."),
                 ("U", "Built the book like a machine, every part in its place, and won the prize for it."),
                 ("B G", "Wrote the hard truth of their own people's lives, and made their name from it.")],
       meets="need:meaning+.1 need:autonomy+.05 res:money+.05 res:time-.05",
       ages=(22, 100), share=.0001,   # estimate: writers who win a national prize for writing or are read in schools
       say="a celebrated author",
       gained="'a national prize for writing' after years as a [novelist] with a [book in print]",
       lost="the next books selling less; the prize stays",
       needs="[novelist] for years; [book in print]; [a publishing contract] or [a prize for writing] usually first"),
]

# ---------------------------------------------------------------- status
TITLES += [
  dict(name="art school student", kind="status", ways="", lasts=3,
       meets="need:competence+.08 need:belonging+.05 res:money-.05 res:time-.1",
       ages=(17, 45), share=.015,   # estimate: creative arts and design is about 1 university student in 12 in the UK;
                                    # fine art, illustration and design together about a third of that
       say="an art student",
       gained="'art school applications' with a portfolio, after [drawing and painting] at school or a foundation year",
       lost="graduating ([art school degree]), dropping out, the fees",
       needs="[drawing and painting] and a portfolio; [savings], a [scholarship] or a student loan"),
]

# ---------------------------------------------------------------- perks: skills (single R)
PERKS += [
  dict(name="writing poems", kind="skill", ways="R", odds=.04, skill_half=15, retires=None,
       ages=(10, 100), share=.03,   # estimate: about 3 lives in 100 keep writing poems past school
       say="writes poems",
       gained="a notebook kept since school, [open-mic poet] nights, a workshop at the library",
       lost="years without writing a line",
       needs="something to say and the habit of writing it down"),
  dict(name="illustration", kind="skill", ways="U B", odds=.05, skill_half=10, retires=None,
       ages=(14, 90), share=.004,   # estimate
       say="can illustrate",
       gained="[art school student], a design course, years of drawing to a brief as an [illustrator for hire]",
       lost="years without drawing to a brief",
       needs="[drawing and painting]"),
  dict(name="sculpting", kind="skill", ways="G W", odds=.04, skill_half=15, retires=None,
       ages=(12, 95), share=.004,   # estimate
       say="can sculpt",
       gained="clay at school, [art school student], the stone yard of a [master craftsperson], years at the wheel",
       lost="years without working the material",
       needs="a place to work and the time"),
]

# ---------------------------------------------------------------- perks: credentials (single U)
PERKS += [
  dict(name="art school degree", kind="credential", ways="U", odds=0, skill_half=None, retires=None,
       ages=(20, 100), share=.012,   # estimate: most art students finish
       say="has an art degree",
       gained="three years as an [art school student], and the degree show",
       lost="never",
       needs="[art school student]"),
  dict(name="a publishing contract", kind="credential", ways="B R", odds=0, skill_half=None, retires=None,
       ages=(16, 100), share=.002,   # estimate: a contract for a book of one's own, with a publisher
       say="has a publisher",
       gained="'a publisher reads the manuscript', an agent's call, a prize for a first book",
       lost="the book not selling, the publisher closing, the contract ending",
       needs="a finished manuscript ([writing stories] or [writing poems])"),
  dict(name="a maker's hallmark", kind="credential", ways="W G", odds=0, skill_half=None, retires=None,
       ages=(20, 100), share=.001,   # estimate: a guild's or a craft council's mark, earned by a piece judged
       say="has a maker's mark",
       gained="a masterpiece judged by the guild or the craft council, after years as a [craft maker]",
       lost="never",
       needs="[craft maker] for years; [workshop] or [tools of one's own]"),
]

# ---------------------------------------------------------------- perks: standing (single B)
PERKS += [
  dict(name="a name in the art world", kind="standing", ways="B", odds=.05, skill_half=10, retires=None,
       ages=(18, 100), share=.0008,   # estimate
       say="has a name in the art world",
       gained="'the first show' that sells out, a critic's review, a dealer who pushes the work, a [following online]",
       lost="years without a show; fashion moving on",
       needs="work shown in public"),
  dict(name="a prize for writing", kind="standing", ways="W U", odds=.04, skill_half=25, retires=None,
       ages=(14, 100), share=.0008,   # estimate: national and regional prizes, first-book prizes, poetry competitions
       say="has won a prize for writing",
       gained="a competition entered, a first book shortlisted, 'a national prize for writing'",
       lost="slowly forgotten",
       needs="[writing poems] or [writing stories]; work sent in"),
  dict(name="a mural the town loves", kind="standing", ways="R G", odds=.04, skill_half=20, retires=None,
       ages=(14, 100), share=.001,   # estimate
       say="painted a mural the town loves",
       gained="'a wall that needs a mural' painted well, the best wall of a [street artist], a school hall painted "
              "with the children",
       lost="the wall knocked down or painted over",
       needs="a wall, and leave to paint it (or none)"),
]

# ---------------------------------------------------------------- perks: bonds (single W)
PERKS += [
  dict(name="pupils who remember you", kind="bond", ways="W", odds=.04, skill_half=15, retires=None,
       ages=(25, 100), share=.003,   # estimate
       say="has pupils who remember them",
       gained="years as an [art teacher], a class at the [life-drawing regular]'s society, an apprentice in the "
              "workshop",
       lost="slowly, as the years pass",
       needs="teaching someone for years"),
  dict(name="a dealer who sells your work", kind="bond", ways="B U", odds=.05, skill_half=5, retires=None,
       ages=(18, 100), share=.0008,   # estimate
       say="has a dealer",
       gained="'the first show' that sells, a [gallery owner] who believes in the work, an art fair",
       lost="the dealer's gallery closing, a falling-out, the work not selling",
       needs="work shown in public"),
  dict(name="a circle of artists", kind="bond", ways="R G", odds=.04, skill_half=6, retires=None,
       ages=(15, 100), share=.008,   # estimate: the friends from the class, the studio block, the poetry night
       say="has a circle of artists",
       gained="years as a [life-drawing regular] or an [open-mic poet], a shared studio, [art school student]",
       lost="drifting apart, a move away",
       needs="time with other people who make things"),
]

# ---------------------------------------------------------------- perks: assets (single G)
PERKS += [
  dict(name="a body of work", kind="asset", ways="G", odds=0, skill_half=None, retires=None,
       ages=(20, 100), share=.003,   # estimate: years of finished work, kept, catalogued or stacked in the shed
       say="has a body of work",
       gained="ten years as a [painter or sculptor], [illustrator for hire], [master craftsperson] or [novelist]",
       lost="a fire or a flood, a clear-out after death",
       needs="years of finished work kept"),
  dict(name="works in collectors' hands", kind="asset", ways="B W", odds=0, skill_half=None, retires=None,
       ages=(20, 100), share=.0006,   # estimate
       say="has work in collections",
       gained="'the first show' that sells, [a dealer who sells your work], 'a work in the national collection'",
       lost="never, though the prices can fall",
       needs="work sold"),
  dict(name="royalties", kind="asset", ways="U R", odds=0, skill_half=None, retires=None,
       ages=(18, 100), share=.001,   # estimate: a book, a picture book or a set of illustrations that keeps earning
       say="earns royalties",
       gained="[a publishing contract] and a book that keeps selling; illustrations licensed again and again",
       lost="the book going out of print",
       needs="[a publishing contract] or work licensed"),
]
