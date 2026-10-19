# Chroma content pack: The Five Callings. The public callings' ladders, for aims version 1 (chroma-ideas/
# next-table-2026-10-19/plan.md, section 5: "Then the missing faces that keep each colour pair fair"). Pathways and
# packs thread, 2026-10-19.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims switch is on and `callings` is in batch.PACKS, so it
# changes no life. The format is set out in chroma-packs/tools/check_aims.py, which checks it.
#
# The four packs' twenty callings give every colour pair two faces and no single colour one (chroma-packs/notes/
# v24-aims-ladders.md). These five are the single colours, one per road, as the Vision thread agreed (10-19 12:04 UTC):
# the faith leader (W), the inventor (U), the magnate (B), the commander (R) and the healer (G). Each is a tendency,
# never a wall: every colour can climb every ladder, and the ladder's face only says which colour it suits best. Tops
# read as the Engine's heights: the Known rung (a sphere's rung 4 or 5), Notable (the summit, known across the country)
# and Historic (the head of an order, or a work that outlives them).

AIMS_CALLINGS = {
    # W, the faith leader: from the minister's rites to the head of an order
    "to lead a faith": dict(
        face="W", domain="faith", sphere="faith",
        dreams=["a life serving one's faith", "a priest of the temple", "to keep the clan's rites"],
        tribal="to keep the rites for all the bands", magic="to be high priest of a god's order",
        steps=[
            dict(say="a life of worship", any=["regular worshipper", "lay religious teacher", "scripture",
                                               "leading a ceremony"]),
            dict(say="ordained, or vowed to an order", any=["ordained religious minister",
                                                            "member of a monastic community", "preaching"]),
            dict(say="a great congregation of your own", any=["senior cleric", "a flock that follows you"],
                 req="was('ordained religious minister') | was('member of a monastic community')", height="Known"),
            dict(say="a voice the whole country hears", any=["known across the country"],
                 req="was('senior cleric') | (yrs_has('member of a monastic community') >= 15)", height="Notable"),
            dict(say="at the head of the order", any=["head of a faith order", "a work that outlives you"],
                 req="was('senior cleric') | was('member of a monastic community')", height="Historic"),
        ]),
    # U, the inventor: from the shed and the trade to a thing the world uses
    "to invent something the world uses": dict(
        face="U", domain="career", sphere="prod",
        dreams=["an inventor"],
        tribal="to make a tool every band will make after you", magic="to be the realm's artificer",
        steps=[
            dict(say="taking things apart", any=["fixing things", "repair-cafe volunteer", "prototyping",
                                                 "apprentice"]),
            dict(say="a technical trade", any=["software developer", "civil engineer", "machinist", "electrician",
                                               "founder of a firm"]),
            dict(say="living from your inventions", any=["inventor", "a patent of your own"],
                 req="was('inventor') | has('prototyping')", height="Known"),
            dict(say="a thing in every home", any=["celebrated inventor", "an invention in everyday use"],
                 height="Notable"),
            dict(say="an invention that outlives you", any=["a work that outlives you"],
                 req="was('inventor')", height="Historic"),
        ]),
    # B, the magnate: from the till to a business empire
    "to build an empire": dict(
        face="B", domain="career", sphere="comm",
        dreams=["a business of one's own", "to reach the top of a big firm", "to build up the family firm",
                "a shop of one's own, with a till that rings"],
        tribal="to be the trader owed a favour in every camp", magic="to be a merchant prince",
        steps=[
            dict(say="a head for a deal", any=["selling", "striking a deal", "shop assistant", "club treasurer"]),
            dict(say="a business of your own", any=["shop owner", "founder of a firm", "café or bar owner"]),
            dict(say="at the head of a large firm", any=["chief executive", "investors who back you"],
                 req="was('chief executive') | was('founder of a firm') | was('shop owner')", height="Known"),
            dict(say="an empire", any=["magnate", "a business empire"], height="Notable"),
            dict(say="a house that outlives you", any=["a work that outlives you"],
                 req="was('magnate') | was('chief executive')", height="Historic"),
        ]),
    # R, the commander: from the team to the general staff
    "to command an army": dict(
        face="R", domain="career", sphere="prot",
        dreams=["an officer in the army", "a general of the realm"],
        tribal="to be the war leader of the clans", magic="to be a warlord, general of the realm",
        steps=[
            dict(say="the one others follow", any=["team captain", "scout or guide", "keeping fit",
                                                   "national service done"]),
            dict(say="a soldier", any=["soldier", "leading soldiers"]),
            dict(say="an officer", any=["army officer", "mentioned in dispatches"],
                 req="was('soldier') | was('army officer')", height="Known"),
            dict(say="a general", any=["general"], height="Notable"),
            dict(say="a name the army keeps", any=["a work that outlives you"], req="was('general')",
                 height="Historic"),
        ]),
    # G, the healer: from the sickbed at home to the healer every family sends for
    "to be a healer": dict(
        face="G", domain="career", sphere="care",
        dreams=["a healer", "a nurse", "a doctor"],
        tribal="to be the healer every band sends for", magic="to be a druid-healer known across the realm",
        steps=[
            dict(say="hands that help", any=["home nursing", "first-aid certificate", "hospice volunteer",
                                             "care worker"]),
            dict(say="a healer by trade", any=["nurse", "midwife", "physician", "paramedic"]),
            dict(say="the one in charge on the ward", any=["senior nurse or midwife", "families who send for you"],
                 req="was('nurse') | was('midwife') | was('physician')", height="Known"),
            dict(say="known across the land", any=["renowned healer"], height="Notable"),
            dict(say="a place of healing that outlives you", any=["a work that outlives you"],
                 req="was('renowned healer') | has('a clinic of your own')", height="Historic"),
        ]),
}

# Who on these roads can earn [a work that outlives you] (core/legacy.py): the head of an order for years; an invention
# in every home; an empire held for a generation; a general's years in command; a healer known for years, or a place of
# healing kept for half a working life.
LEGACY_CALLINGS = ("(age >= 40) & ((yrs_has('head of a faith order') >= 5) | "
                   "((yrs_has('celebrated inventor') >= 3) & has('an invention in everyday use')) | "
                   "(yrs_has('magnate') >= 8) | (yrs_has('general') >= 4) | (yrs_has('renowned healer') >= 5) | "
                   "((yrs_has('a clinic of your own') >= 15) & has('families who send for you')))")
