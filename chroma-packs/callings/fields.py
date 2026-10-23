# Chroma content pack: The Five Callings. The aim fields (aims version 2): the five single-colour callings of aims.py
# (AIMS_CALLINGS) as fields on the Engine's ladder shapes, with a clock on every rung. Pathways and packs thread,
# 2026-10-23, for v25 (brief: chroma-ideas/v25-prep/packs/fields/BRIEF.md; Emren's decision #9 in
# chroma-ideas/next-table-2026-10-19/v25-decisions-emren.md, section 5).
#
# SWITCHED OFF: nothing reads this file until the Engine's aims_v2 is on and the pack is in batch.PACKS, so it changes
# no life. With aims_v2 off, v1 reads aims.py as before.
#
# The format is the Engine's frozen aims shape: chroma-engine/notes/v25/aims-shape.md, sections 3 and 8 (the chess
# entry, key for key, with demand, window, upkeep, prep and meets); chroma-packs/tools/check_fields.py checks it.
# Shapes: the faith leader on the faith shape (seeking, belonging, serving, guiding, a teacher remembered), the inventor
# on the craft shape (learner, journeyman, trusted hand, master, a name in the craft), the magnate, the commander and
# the healer on the career shape (a foot in, established, senior, leading, the top). Five rungs each, none skipped.
# v1 is kept exactly: the name, face, sphere, domain, dreams (none of the five has new dreams in core/dreams.py),
# tribal and magic, and each step's say, any, req and height. calling=True: every road leads to a height.
#
# Clocks. `years` is (median, 10th, 90th percentile) of steady effort from the rung below, set from training lengths
# and from the years the pack's own rules ask (roles.py's yrs_has, the gates in engine-conditions.py: a senior cleric
# from 35 after 8 years ordained, an inventor after 3 years at a trade, a chief executive from 28 after 3 years as a
# founder, officer selection from 20 to 45 after 3 years as a soldier, a general after 15 years as an officer, a
# senior nurse or midwife after 5 years on the ward). A rung's low is never below the years its moment's gate asks
# (engine-conditions.py, often a year or two under roles.py's), and the Historic rungs follow core/legacy.py through
# LEGACY_CALLINGS (years held at the summit). `share` is of those who keep at it, the share who reach the rung, so the
# shares multiply down the ladder; the products at the Known rung and at the top were checked against the catalogue's
# share= of the Known titles and summits (catalogue.py and its sources). `start` puts best_to at or above the youngest
# first age of rung 1's names (catalogue ages=). `demand` hours are free hours a week outside paid work (where the
# rung's title is the job, only the extra: study, boards, training); money and entry are shares of a year's free
# money. `window` is set only where the step really has outside timing (a yearly intake, a selection board, an age
# limit: the pack's own where its rules name one, else an estimate), `upkeep` only where a benefit really fades without
# use; a title held for life as an achievement has none. Sources are named in the comment above each field; "estimate"
# where no count is known. Words a player reads name no real faith, order, firm, army, country or person.
#
# A sixth calling, the druid's "to keep the land" (the steward of the land, with Outer world's land.json), is written
# and held as FIELDS_LAND in druid.py, which nothing loads; the Engine joins it here behind aims_v2 (PACK.md, "The
# sixth road"). Its place is marked at the end.

FIELDS_CALLINGS = {
    # W, the faith leader. Clock: ordination follows a degree and two to three years at a faith's college, or a
    # discernment year, a novitiate and years of first vows before life vows (estimate across faiths: 4 to 15 years
    # from a life of worship); roles.py: a senior cleric from 35 after 8 years ordained or 10 in an order (its moment's
    # gate from 6 or 8), the head of an order from 45 after 8 years as a senior cleric or 20 in an order; catalogue:
    # about 1 minister in 8 leads a great congregation (.0005 against .004); national voices and heads: estimate (the
    # head .00002, about 1 senior cleric in 25). Sum 20 years to Known, 36 to the top; top .9 x .4 x .3 x .1 x .15.
    "to lead a faith": dict(
        shape="faith", face="W", sphere="faith", domain="faith", calling=True,
        dreams=["a life serving one's faith", "a priest of the temple", "to keep the clan's rites"],
        thing="the ministry", doing="serving the faith", contest="the council's choosing",
        places=["faith.congregation", "faith.orders", "learn.higher"],
        prep=["faith practice", "public speaking", "reading"], meets=["meaning", "belonging"],
        people=dict(coach="an old minister who lets them lead the prayers",
                    rival="another candidate with a finer voice", peer="the others training for the ministry",
                    patron="an elder of the faith who puts their name forward"),
        round=["a small community across town that needs a lay leader",
               "a faith's college that takes older students", "the study circle that meets every week"],
        below="{N} gives the sparrow found under the hedge a proper send-off, with a reading, a song and a few words",
        tribal="to keep the rites for all the bands", magic="to be high priest of a god's order",
        rungs=[
            dict(say="a life of worship", any=["regular worshipper", "lay religious teacher", "scripture",
                                               "leading a ceremony"],
                 years=(2, 0.5, 5), share=0.9, start=(10, 25, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.03, entry=0, energy=0.15), window=None, upkeep=None),
            # the faiths' colleges and houses take students and novices once a year; a minister without a post for
            # years loses the faith's leave to lead worship and drops off its list for appointments (estimate)
            dict(say="ordained, or vowed to an order", any=["ordained religious minister",
                                                            "member of a monastic community", "preaching"],
                 years=(8, 4, 15), share=0.4, contests_y=1, forks=["go_on", "pay"],
                 demand=dict(hours=12, money=0.15, entry=0.2, energy=0.5),
                 window=dict(every=1, open_weeks=12),
                 upkeep=dict(of="access", years=5, kept_by=["leading worship", "teaching"])),
            dict(say="a great congregation of your own", any=["senior cleric", "a flock that follows you"],
                 req="was('ordained religious minister') | was('member of a monastic community')", height="Known",
                 years=(10, 6, 18), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="a voice the whole country hears", any=["known across the country"],
                 req="was('senior cleric') | (yrs_has('member of a monastic community') >= 15)", height="Notable",
                 years=(8, 3, 20), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            # most heads of a faith or an order serve for life, so the seat has no fixed term (catalogue)
            dict(say="at the head of the order", any=["head of a faith order", "a work that outlives you"],
                 req="was('senior cleric') | was('member of a monastic community')", height="Historic",
                 years=(8, 4, 15), share=0.15, contests_y=0.5, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # U, the inventor. Clock: a technical trade takes an apprenticeship of 3 to 4 years or an engineering degree of 3
    # to 4, a self-taught programmer a year or two (rung 2); roles.py: an inventor after 3 years at a trade or 2 as a
    # founder (the moment from 2), a celebrated inventor after 5 as an inventor (the moment from 4); Jones, "The Burden
    # of Knowledge" (2009): first patents come at about 30 on average, later each decade; Bell, Chetty, Jaravel,
    # Petkova and Van Reenen (2019): about 1.6 in 1,000 hold a patent by their thirties (catalogue); legacy.py: 3 years
    # celebrated with an invention in everyday use, from 40. Celebrated inventors: estimate (catalogue .00005, about 1
    # inventor in 10). Sum 14.5 years to Known, 28.5 to the top; top .9 x .6 x .15 x .1 x .2.
    "to invent something the world uses": dict(
        shape="craft", face="U", sphere="prod", domain="career", calling=True,
        dreams=["an inventor"],
        thing="the invention", doing="inventing", contest="an inventors' fair",
        places=["prod.craft", "learn.higher"], prep=["the craft", "study", "numbers"], meets=["competence", "autonomy"],
        people=dict(coach="an old engineer who lets them use the lathe",
                    rival="someone across town after the same idea", peer="the regulars at the repair café",
                    patron="a backer who likes a working model"),
        round=["a firm that takes on apprentices late", "a night course in engineering",
               "the makers' club that meets every week"],
        below="{N} takes the alarm clock apart to see how it works, and it goes back together with a piece left over",
        tribal="to make a tool every band will make after you", magic="to be the realm's artificer",
        rungs=[
            dict(say="taking things apart", any=["fixing things", "repair-cafe volunteer", "prototyping",
                                                 "apprentice"],
                 years=(1.5, 0.5, 4), share=0.9, start=(8, 16, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.03, entry=0.03, energy=0.3), window=None, upkeep=None),
            # apprenticeships and degree courses take their intake once a year; a technical skill goes stale after
            # some years away from the work (estimate)
            dict(say="a technical trade", any=["software developer", "civil engineer", "machinist", "electrician",
                                               "founder of a firm"],
                 years=(4, 2, 7), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=12, money=0.25, entry=0.3, energy=0.55),
                 window=dict(every=1, open_weeks=8),
                 upkeep=dict(of="proficiency", years=5, kept_by=["work", "the craft"])),
            dict(say="living from your inventions", any=["inventor", "a patent of your own"],
                 req="was('inventor') | has('prototyping')", height="Known",
                 years=(9, 3, 20), share=0.15, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=10, money=0.15, entry=0.2, energy=0.55), window=None, upkeep=None),
            dict(say="a thing in every home", any=["celebrated inventor", "an invention in everyday use"],
                 height="Notable",
                 years=(8, 4, 18), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.1, entry=0.1, energy=0.5), window=None, upkeep=None),
            dict(say="an invention that outlives you", any=["a work that outlives you"],
                 req="was('inventor')", height="Historic",
                 years=(6, 3, 15), share=0.2, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=5, money=0.05, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # B, the magnate. Clock: Azoulay, Jones, Kim and Miranda, "Age and High-Growth Entrepreneurship" (2020): founders
    # of new firms are about 42 on average and of the fastest-growing about 45, so a business of one's own usually
    # comes a decade or more into working life (shops and cafés sooner); roles.py: a chief executive from 28 after 3
    # years as a founder or 5 as a shop or café owner (the moment from 3 or 4), a magnate after 5 as a chief executive
    # or 10 as a founder (the moment from 4 or 8); legacy.py: 8 years a magnate. BLS (May 2023): about 200,000 chief
    # executives (catalogue .002); magnates: estimate (.00005, about 1 chief executive in 40). Sum 18.5 years to Known,
    # 36.5 to the top; top .9 x .45 x .15 x .05 x .3.
    "to build an empire": dict(
        shape="career", face="B", sphere="comm", domain="career", calling=True,
        dreams=["a business of one's own", "to reach the top of a big firm", "to build up the family firm",
                "a shop of one's own, with a till that rings"],
        thing="the business", doing="building the business", contest="a pitch to the backers",
        places=["comm.market", "comm.shop", "comm.credit"], prep=["the market", "numbers", "leading people"],
        meets=["autonomy", "competence"],
        people=dict(coach="an old trader who shows them how to read the books",
                    rival="a rival who opens across the street", peer="the other shopkeepers on the street",
                    patron="a backer who likes the numbers"),
        round=["a market stall to start small", "a partner with the money the bank will not lend",
               "the traders' breakfast every month"],
        below="{N} sells old comics from a box at the gate, and knows exactly which ones pay",
        tribal="to be the trader owed a favour in every camp", magic="to be a merchant prince",
        rungs=[
            dict(say="a head for a deal", any=["selling", "striking a deal", "shop assistant", "club treasurer"],
                 years=(1.5, 0.5, 4), share=0.9, start=(12, 30, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            # the stake: savings or a loan into the lease, the stock and the first wages
            dict(say="a business of your own", any=["shop owner", "founder of a firm", "café or bar owner"],
                 years=(10, 3, 20), share=0.45, contests_y=1, forks=["pay", "round"],
                 demand=dict(hours=12, money=0.2, entry=0.5, energy=0.65), window=None, upkeep=None),
            # the backers drift away after years out of business (catalogue: [investors who back you])
            dict(say="at the head of a large firm", any=["chief executive", "investors who back you"],
                 req="was('chief executive') | was('founder of a firm') | was('shop owner')", height="Known",
                 years=(7, 3, 15), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.05, entry=0.1, energy=0.7), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["work", "the market"])),
            # buying the rival firm: savings or shares (the moment's requires)
            dict(say="an empire", any=["magnate", "a business empire"], height="Notable",
                 years=(8, 4, 20), share=0.05, contests_y=1, forks=["take", "pay"],
                 demand=dict(hours=8, money=0.1, entry=0.5, energy=0.7), window=None, upkeep=None),
            dict(say="a house that outlives you", any=["a work that outlives you"],
                 req="was('magnate') | was('chief executive')", height="Historic",
                 years=(10, 8, 20), share=0.3, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
        ]),

    # R, the commander. Clock: most recruits join at 17 to 24, basic training takes 10 to 14 weeks and most armies take
    # recruits to about 35 (estimate); roles.py: officer selection from 20 to 45 after 3 years as a soldier, or a degree
    # and the academy (the moment from 20 to 40, after 2); a general after 15 years as an officer (the moment from 12,
    # at 40 to 62, the post retired at 62); a first general's star commonly comes 20 to 25 years into a commission
    # (estimate); legacy.py: 4 years a general. US Department of Defense: about 1 in 6 on active duty is an officer,
    # under 1,000 generals and admirals at a time (catalogue .006 and .00003). Sum 8 years to Known, 33 to the top; top
    # .9 x .6 x .25 x .025 x .3.
    "to command an army": dict(
        shape="career", face="R", sphere="prot", domain="career", calling=True,
        dreams=["an officer in the army", "a general of the realm"],
        thing="the army", doing="soldiering", contest="the selection board",
        places=["prot.host", "gather.games"], prep=["fitness", "leading people", "organising"],
        meets=["belonging", "meaning"],
        people=dict(coach="a sergeant who makes recruits into soldiers", rival="a cadet who wants the same command",
                    peer="the section", patron="a colonel who remembers their name"),
        round=["a degree first, then the academy", "a transfer to another regiment",
               "the reserves' training weekend, every month"],
        below="{N} sorts the street's children into sides for the snowball fight, and their side always holds the wall",
        tribal="to be the war leader of the clans", magic="to be a warlord, general of the realm",
        rungs=[
            dict(say="the one others follow", any=["team captain", "scout or guide", "keeping fit",
                                                   "national service done"],
                 years=(2, 0.5, 5), share=0.9, start=(10, 18, 26), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.02, entry=0.02, energy=0.45), window=None, upkeep=None),
            # no recruit taken after about 35; a soldier's fitness fades within a couple of years out of training
            dict(say="a soldier", any=["soldier", "leading soldiers"],
                 years=(2, 0.5, 5), share=0.6, contests_y=1, forks=["go_on"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6),
                 window=dict(deadline_age=35),
                 upkeep=dict(of="proficiency", years=2, kept_by=["training", "work"])),
            # officer selection: a board each year, no entry after 45 (roles.py: age <= 45)
            dict(say="an officer", any=["army officer", "mentioned in dispatches"],
                 req="was('soldier') | was('army officer')", height="Known",
                 years=(4, 2, 8), share=0.25, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=6, money=0.03, entry=0.05, energy=0.6),
                 window=dict(every=1, open_weeks=10, deadline_age=45), upkeep=None),
            # the promotion board sits once a year; the moment comes from 40 to 62, when the post retires
            dict(say="a general", any=["general"], height="Notable",
                 years=(20, 13, 26), share=0.025, contests_y=1, forks=["go_on", "take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.65),
                 window=dict(every=1, open_weeks=8, deadline_age=62), upkeep=None),
            dict(say="a name the army keeps", any=["a work that outlives you"], req="was('general')",
                 height="Historic",
                 years=(5, 4, 9), share=0.3, contests_y=0.5, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),

    # G, the healer. Clock: a nursing or midwifery degree takes 3 to 4 years (rung 2); the catalogue's NHS figure puts
    # about 1 nurse or midwife in 8 at band 7 or above (rung 3) after 5 or more years on the ward (roles.py:
    # yrs_has('nurse') >= 5, the moment from 4); roles.py: a renowned healer after 10 years of the career (the moment
    # from 4 years in charge, or 10 to 12 on the wards); legacy.py: 5 years renowned, or a clinic of one's own kept 15
    # years. Renowned healers and places of healing: estimate (catalogue .00005, about 1 senior nurse in 80). Sum 10.5
    # years to Known, 26.5 to the top; top .9 x .45 x .3 x .04 x .25.
    "to be a healer": dict(
        shape="career", face="G", sphere="care", domain="career", calling=True,
        dreams=["a healer", "a nurse", "a doctor"],
        thing="nursing", doing="looking after the sick", contest="the ward inspection",
        places=["care.houses", "learn.higher"], prep=["care", "study"], meets=["meaning", "competence"],
        people=dict(coach="a ward sister who trains the new nurses", rival="a nurse on the same ward",
                    peer="the night shift", patron="a consultant who notices good work"),
        round=["a care home that takes trainees", "the evening course at the college",
               "the volunteers' rota at the hospice, every week"],
        below="{N} brings the neighbour's sick cat a saucer of milk every morning and checks it is still breathing",
        tribal="to be the healer every band sends for", magic="to be a druid-healer known across the realm",
        rungs=[
            dict(say="hands that help", any=["home nursing", "first-aid certificate", "hospice volunteer",
                                             "care worker"],
                 years=(1, 0.5, 3), share=0.9, start=(12, 25, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            # the courses take their intake once a year; the registration lapses after about 5 years out of practice
            dict(say="a healer by trade", any=["nurse", "midwife", "physician", "paramedic"],
                 years=(3.5, 3, 6), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=12, money=0.25, entry=0.3, energy=0.6),
                 window=dict(every=1, open_weeks=10),
                 upkeep=dict(of="credential", years=5, kept_by=["work", "teaching"])),
            dict(say="the one in charge on the ward", any=["senior nurse or midwife", "families who send for you"],
                 req="was('nurse') | was('midwife') | was('physician')", height="Known",
                 years=(6, 4, 12), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.05, entry=0.05, energy=0.65), window=None, upkeep=None),
            dict(say="known across the land", any=["renowned healer"], height="Notable",
                 years=(8, 4, 18), share=0.04, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.55), window=None, upkeep=None),
            # a clinic, birth centre or hospice of one's own: savings or backers (catalogue: [a clinic of your own])
            dict(say="a place of healing that outlives you", any=["a work that outlives you"],
                 req="was('renowned healer') | has('a clinic of your own')", height="Historic",
                 years=(8, 5, 18), share=0.25, contests_y=0.5, forks=["pay", "go_on"],
                 demand=dict(hours=8, money=0.1, entry=0.3, energy=0.55), window=None, upkeep=None),
        ]),

    # G, the steward of the land (the druid): "to keep the land", held in druid.py as FIELDS_LAND, joins here.
}
