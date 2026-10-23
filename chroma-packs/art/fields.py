# Chroma content pack: Art and Writing. The five callings of aims.py as fields, for aims version 2 (v25, Emren's
# decision #9). Pathways and packs thread, 2026-10-23.
#
# SWITCHED OFF: nothing reads this file until the Engine's aims_v2 is on and the pack is in batch.PACKS. Plain data;
# nothing is imported and nothing runs. The format is the Engine's frozen aims shape (chroma-engine/notes/v25/
# aims-shape.md in the shared folder, sections 3 and 8: the chess entry is the template); check_fields.py in
# ../tools checks it.
#
# Each field keeps its v1 aim (aims.py) as it is: the name, face, sphere, domain, tribal and magic, v1's dreams, and
# each step as a rung with its say, any, req and height unchanged. The dreams of core/dreams.py's AIM_DREAMS follow
# v1's (a name v1 already has is not repeated). Shapes: the writer, the painter and the illustrator are the art shape
# (trying, showing, a following, recognised, a body of work), the one who brings art to the people the cause shape
# (caring, joining, organising, leading, a change that lasts), the maker the craft shape (learner, journeyman, trusted
# hand, master, a name in the craft); every shape has five rungs, so no field skips one.
#
# How the clocks were set. `years` is (median, 10th, 90th percentile) of steady effort from the rung below: the course
# lengths (art school three years, the catalogue's lasts=3; an apprenticeship three to four), the years a title needs
# in roles.py (yrs_has, yrs_career) and in the legacy rule (aims.py LEGACY_ART: six years as a renowned artist or a
# celebrated author, twenty as a master or a gallery owner), and estimates where nothing is counted, each named in the
# comment above its field. `share` is of those who keep at it, the share who reach the rung; the shares multiply down
# the ladder and were checked against the catalogue's share= of the rung's titles (a summit held by 1 life in 10,000
# is reached by well under 1 in 100 of those who try). `demand` is at steady intensity, outside paid work: hours a
# week, money a year and a one-time entry as shares of a year's free money, and how tiring it is. `window` names an
# external timing only where the step has one (a yearly prize season, the guild's yearly judging); `upkeep` names the
# one part that really fades without use (a publisher's door, a client list, the hand's skill), never an achievement.

FIELDS_ART = {
    # Clock: estimate from writers' paths (drafts for some years before a first book in print, often in the thirties;
    # readers and a prize some years after); roles.py: a celebrated author has been a novelist 3 years with a book in
    # print; LEGACY_ART: 6 years as one, from age 40. About 1 in 10 of those who keep at it reach Known, 6 in 1,000 the
    # summit (celebrated authors are about 1 life in 10,000, novelists 5 in 10,000: the catalogue).
    "to write books": dict(
        shape="art", face="R W", sphere="arts", domain="career", calling=True,
        dreams=["a writer of books", "a maker of verses", "a chronicler of the realm"],
        thing="the book", doing="writing", contest="a writing competition",
        places=["arts.page", "gather.house", "learn.keeping"], prep=["writing", "reading"],
        meets=["meaning", "autonomy"],
        people=dict(coach="a writer who runs the workshop at the library",
                    rival="a writer from the same group whose book came out first",
                    peer="the writing group", patron="an editor who believes in the book"),
        round=["a small press that reads manuscripts sent without an agent", "printing the book yourself",
               "the writing group at the library, every week"],
        below="{N} fills the back pages of every exercise book with stories and will not let anyone read the endings",
        tribal="to make the verses every band repeats", magic="to be chronicler of the realm",
        rungs=[
            dict(say="words of your own", any=["open-mic poet", "writing poems", "writing stories"],
                 years=(1, 0.5, 3), share=0.9, start=(10, 25, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="a writer", any=["novelist", "book in print", "a publishing contract"],
                 years=(4, 2, 10), share=0.3, contests_y=2, forks=["pay", "round"],
                 demand=dict(hours=8, money=0.03, entry=0.05, energy=0.5), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["writing", "work"])),
            dict(say="people read you", any=["a prize for writing", "royalties", "name on the local scene"],
                 req="was('novelist') | was('open-mic poet') | has('book in print')", height="Known",
                 years=(4, 2, 10), share=0.35, contests_y=3, forks=["take"],
                 demand=dict(hours=10, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a celebrated author", any=["celebrated author"], height="Notable",
                 years=(6, 3, 15), share=0.06, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.02, entry=0, energy=0.5),
                 window=dict(every=1, open_weeks=8), upkeep=None),
            dict(say="a book that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(8, 6, 20), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: art school takes 3 years (catalogue lasts=3); roles.py: a painter has been at art school, or 4 years in
    # the life class, 2 on the walls or 3 drawing for hire, and a renowned artist 5 years in a career; LEGACY_ART: 6
    # years as one. Arts Council England's surveys (few visual artists live on their practice) for the low share at
    # rung 2; the rest estimate. About 5 in 100 reach Known, 3 in 1,000 the summit (renowned artists: 1 life in 10,000).
    "to make art people stop for": dict(
        shape="art", face="R G", sphere="arts", domain="career", calling=True,
        dreams=["an artist", "a painter of the cave walls", "a court painter"],
        thing="the painting", doing="painting", contest="an open exhibition",
        places=["arts.craft", "gather.hall", "learn.higher"], prep=["drawing"], meets=["meaning", "autonomy"],
        people=dict(coach="a painter who runs the life class", rival="a painter from the same studios who sells first",
                    peer="the life-drawing class", patron="a collector who buys early"),
        round=["walls painted for nothing until someone pays", "a studio shared across town",
               "the open life class at the community centre, every week"],
        below="{N} draws on every envelope and steamed-up window, and stops in the street to look at the light",
        tribal="to paint the cave every band visits", magic="to be court painter",
        rungs=[
            dict(say="drawing every day", any=["life-drawing regular", "drawing and painting", "art school student"],
                 years=(1, 0.5, 3), share=0.9, start=(5, 18, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.03, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="making art for a living", any=["street artist", "painter or sculptor"],
                 years=(4, 2, 10), share=0.15, contests_y=2, forks=["pay", "take"],
                 demand=dict(hours=10, money=0.1, entry=0.15, energy=0.6), window=None, upkeep=None),
            dict(say="the town knows your work", any=["a mural the town loves", "a name in the art world",
                                                      "a circle of artists"], height="Known",
                 years=(4, 2, 8), share=0.4, contests_y=3, forks=["take"],
                 demand=dict(hours=10, money=0.08, entry=0.05, energy=0.5), window=None,
                 upkeep=dict(of="access", years=5, kept_by=["work", "the craft"])),
            dict(say="a renowned artist", any=["renowned artist"], height="Notable",
                 years=(8, 4, 18), share=0.05, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=10, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a work that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(8, 6, 20), share=0.25, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: roles.py: an illustrator for hire has been at art school (3 years) or 2 years in the life class, with a
    # portfolio; work that keeps earning (royalties, a dealer) some years after, estimate; LEGACY_ART: 6 years as a
    # renowned artist. The catalogue's freelance illustrators are about 3 lives in 1,000 (the BLS counts only the
    # employed ones). About 7 in 100 reach Known, 6 in 1,000 the country's notice.
    "to draw for a living": dict(
        shape="art", face="U B", sphere="arts", domain="career", calling=True,
        dreams=["an illustrator", "a maker of patterns", "an illuminator of books"],
        thing="the portfolio", doing="drawing", contest="an illustration competition",
        places=["arts.page", "learn.higher", "gather.circle"], prep=["drawing"], meets=["competence", "autonomy"],
        people=dict(coach="a tutor at the art school who still takes commissions",
                    rival="an illustrator who pitches for the same jobs", peer="the freelancers who share a studio",
                    patron="an art director at a publisher who keeps sending work"),
        round=["a design job that pays while the portfolio grows", "selling prints online",
               "the drawing club that meets at the library, every week"],
        below="{N} draws a comic strip of every family holiday, with the dog as its hero and every face just right",
        tribal="to mark the patterns that are traded far", magic="to be illuminator to the Orders",
        rungs=[
            dict(say="a pencil in hand", any=["art school student", "life-drawing regular", "illustration"],
                 years=(1, 0.5, 3), share=0.9, start=(8, 18, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.03, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="drawing for hire", any=["illustrator for hire", "art school degree"],
                 years=(3, 1.5, 6), share=0.4, contests_y=2, forks=["pay"],
                 demand=dict(hours=10, money=0.1, entry=0.25, energy=0.5), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "drawing"])),
            dict(say="work in demand", any=["royalties", "a publishing contract", "a dealer who sells your work"],
                 req="was('illustrator for hire') | was('art school student')", height="Known",
                 years=(5, 2, 10), share=0.2, contests_y=2, forks=["take"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a name across the country", any=["renowned artist", "known across the country"],
                 req="was('illustrator for hire')", height="Notable",
                 years=(7, 3, 15), share=0.08, contests_y=2, forks=["go_on", "take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="pictures that outlive you", any=["a work that outlives you"], height="Historic",
                 years=(10, 6, 25), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: roles.py: a gallery owner has been a painter 3 years, an art teacher 5, a shop owner or a curator 3, with
    # savings or a patron; LEGACY_ART: 20 years as a gallery owner with works in collectors' hands. Small commercial
    # galleries are a few in each town (catalogue, about 3 lives in 10,000); the rest estimate. About 7 in 100 reach
    # Known, 7 in 1,000 the country's notice.
    "to bring art to the people": dict(
        shape="cause", face="B W", sphere="arts", domain="career", calling=True,
        dreams=["a jeweller to the court"],
        thing="the gallery", doing="showing and selling art", contest="an art fair",
        places=["arts.craft", "comm.market", "learn.keeping"], prep=["the market", "organising"],
        meets=["belonging", "competence"],
        people=dict(coach="a dealer who has run a gallery for thirty years", rival="the gallery across the square",
                    peer="the artists on the books", patron="a collector with a good eye and deep pockets"),
        round=["a pop-up show in an empty shop", "selling online to collectors far away",
               "the art market on the square, every month"],
        below="{N} rearranges the pictures on the walls at home and sells friends' drawings at school for pocket money",
        tribal="to trade carvings at the great gatherings", magic="to keep a picture hall on the square",
        rungs=[
            dict(say="an eye for art", any=["life-drawing regular", "art school student", "museum curator",
                                            "shop owner"],
                 years=(1.5, 0.5, 4), share=0.9, start=(14, 30, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.03, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="works that sell", any=["works in collectors' hands", "a dealer who sells your work",
                                             "premises of one's own"],
                 years=(4, 2, 8), share=0.3, contests_y=2, forks=["pay"],
                 demand=dict(hours=10, money=0.15, entry=0.2, energy=0.5), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "the market"])),
            dict(say="a gallery of your own", any=["gallery owner", "a name in the art world"], height="Known",
                 years=(5, 2, 10), share=0.25, contests_y=3, forks=["pay", "take"],
                 demand=dict(hours=8, money=0.2, entry=0.4, energy=0.6), window=None, upkeep=None),
            dict(say="known across the country", any=["known across the country", "collection of one's own"],
                 req="was('gallery owner')", height="Notable",
                 years=(8, 4, 15), share=0.1, contests_y=2, forks=["take"],
                 demand=dict(hours=8, money=0.1, entry=0, energy=0.5), window=None, upkeep=None),
            dict(say="a collection that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(12, 8, 25), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.1, entry=0, energy=0.4), window=None, upkeep=None),
        ]),

    # Clock: apprenticeships take 3 to 4 years; roles.py: a maker's hallmark after 4 years as a craft maker, a master
    # craftsperson after 5 (a carpenter after 8, with the hallmark); LEGACY_ART: 20 years as a master with the
    # hallmark, or 6 as a renowned artist. Masters are about 8 lives in 10,000 (catalogue, estimate). About 8 in 100
    # reach Known, 4 in 1,000 a renowned name.
    "to master a craft": dict(
        shape="craft", face="G U", sphere="arts", domain="career", calling=True,
        dreams=["the best toolmaker in the clans", "a master of a craft", "a master basket-weaver",
                "a master of the craft guild"],
        thing="the craft", doing="making things by hand", contest="a judged craft show",
        places=["prod.craft", "comm.market", "arts.craft"], prep=["the craft"], meets=["competence", "autonomy"],
        people=dict(coach="a master who takes on one apprentice at a time",
                    rival="the maker at the next stall at the fair", peer="the makers who share the workshop",
                    patron="a buyer who orders a piece every year"),
        round=["the college workshop's evening classes", "a maker out of town who teaches in return for help",
               "the craft market on the square, every month"],
        below="{N} whittles spoons from fallen branches and will not stop until the bowl is smooth enough to sip from",
        tribal="to be the master carver whose work is traded far", magic="to be a master of the craft guild",
        rungs=[
            dict(say="learning the trade", any=["craft maker", "carpenter", "apprentice", "workshop"],
                 years=(1, 0.5, 3), share=0.9, start=(12, 20, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.03, entry=0.05, energy=0.4), window=None, upkeep=None),
            dict(say="work with your mark on it", any=["a maker's hallmark", "sculpting", "apprentice of one's own",
                                                       "tools of one's own"],
                 years=(4, 2, 7), share=0.6, contests_y=1, forks=["pay"],
                 demand=dict(hours=8, money=0.08, entry=0.15, energy=0.5), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["the craft", "teaching"])),
            dict(say="a master of the craft", any=["master craftsperson"], height="Known",
                 years=(7, 4, 15), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0.1, energy=0.5),
                 window=dict(every=1, open_weeks=6), upkeep=None),
            dict(say="a renowned artist", any=["renowned artist"], req="was('master craftsperson')", height="Notable",
                 years=(10, 5, 20), share=0.05, contests_y=1, forks=["go_on", "take"],
                 demand=dict(hours=6, money=0.03, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="a work that outlives you", any=["a work that outlives you"], height="Historic",
                 years=(8, 6, 20), share=0.3, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.3), window=None, upkeep=None),
        ]),
}
