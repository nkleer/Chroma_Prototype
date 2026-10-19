# Chroma content pack: Art and Writing. The public callings' ladders, for aims version 1 (chroma-ideas/
# next-table-2026-10-19/plan.md, section 5). Pathways and packs thread, 2026-10-19.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims switch is on, so it changes no life. The format is set
# out in chroma-packs/tools/check_aims.py, which checks it (a short summary is at the top of ../politics/aims.py).
#
# Five callings over the pack's roads (PACK.md, "The roads"): Red's road holds two of them (the painter and the writer),
# as it is the deepest; the five faces make a ring (R W, W B, B U, U G, G R) and every colour stands in two of them.

AIMS_ART = {
    # R, raw expression (writing): the writer
    "to write books": dict(
        face="R W", domain="career", sphere="arts",
        dreams=[],
        tribal="to make the verses every band repeats", magic="to be chronicler of the realm",
        steps=[
            dict(say="words of your own", any=["open-mic poet", "writing poems", "writing stories"]),
            dict(say="a writer", any=["novelist", "book in print", "a publishing contract"]),
            dict(say="people read you", any=["a prize for writing", "royalties", "name on the local scene"],
                 req="was('novelist') | was('open-mic poet') | has('book in print')", height="Known"),
            dict(say="a celebrated author", any=["celebrated author"], height="Notable"),
            dict(say="a book that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # R, raw expression (paint, walls and stone): the painter
    "to make art people stop for": dict(
        face="R G", domain="career", sphere="arts",
        dreams=[],
        tribal="to paint the cave every band visits", magic="to be court painter",
        steps=[
            dict(say="drawing every day", any=["life-drawing regular", "drawing and painting", "art school student"]),
            dict(say="making art for a living", any=["street artist", "painter or sculptor"]),
            dict(say="the town knows your work", any=["a mural the town loves", "a name in the art world",
                                                      "a circle of artists"], height="Known"),
            dict(say="a renowned artist", any=["renowned artist"], height="Notable"),
            dict(say="a work that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # U, the experimenter: the illustrator
    "to draw for a living": dict(
        face="U B", domain="career", sphere="arts",
        dreams=[],
        tribal="to mark the patterns that are traded far", magic="to be illuminator to the Orders",
        steps=[
            dict(say="a pencil in hand", any=["art school student", "life-drawing regular", "illustration"]),
            dict(say="drawing for hire", any=["illustrator for hire", "art school degree"]),
            dict(say="work in demand", any=["royalties", "a publishing contract", "a dealer who sells your work"],
                 req="was('illustrator for hire') | was('art school student')", height="Known"),
            dict(say="a name across the country", any=["renowned artist", "known across the country"],
                 req="was('illustrator for hire')", height="Notable"),
            dict(say="pictures that outlive you", any=["a work that outlives you"], height="Historic"),
        ]),
    # B, art as a career: the one who brings art to the people who buy it
    "to bring art to the people": dict(
        face="B W", domain="career", sphere="arts",
        dreams=["a jeweller to the court"],
        tribal="to trade carvings at the great gatherings", magic="to keep a picture hall on the square",
        steps=[
            dict(say="an eye for art", any=["life-drawing regular", "art school student", "museum curator",
                                            "shop owner"]),
            dict(say="works that sell", any=["works in collectors' hands", "a dealer who sells your work",
                                             "premises of one's own"]),
            dict(say="a gallery of your own", any=["gallery owner", "a name in the art world"], height="Known"),
            dict(say="known across the country", any=["known across the country", "collection of one's own"],
                 req="was('gallery owner')", height="Notable"),
            dict(say="a collection that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
    # G, the folk maker: the one who masters a craft
    "to master a craft": dict(
        face="G U", domain="career", sphere="arts",
        dreams=["the best toolmaker in the clans"],
        tribal="to be the master carver whose work is traded far", magic="to be a master of the craft guild",
        steps=[
            dict(say="learning the trade", any=["craft maker", "carpenter", "apprentice", "workshop"]),
            dict(say="work with your mark on it", any=["a maker's hallmark", "sculpting", "apprentice of one's own",
                                                       "tools of one's own"]),
            dict(say="a master of the craft", any=["master craftsperson"], height="Known"),
            dict(say="a renowned artist", any=["renowned artist"], req="was('master craftsperson')", height="Notable"),
            dict(say="a work that outlives you", any=["a work that outlives you"], height="Historic"),
        ]),
}

# Who in art and writing can earn [a work that outlives you] (core/legacy.py): years as a renowned artist or a
# celebrated author; a master's hallmark worn for a generation; a gallery whose works went into the collections.
LEGACY_ART = ("(age >= 40) & ((yrs_has('renowned artist') >= 6) | (yrs_has('celebrated author') >= 6) | "
              "((yrs_has('master craftsperson') >= 20) & has(\"a maker's hallmark\")) | "
              "((yrs_has('gallery owner') >= 20) & has(\"works in collectors' hands\")))")
