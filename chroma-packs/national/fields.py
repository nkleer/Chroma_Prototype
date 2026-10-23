# Chroma content pack: National standing. The routes' aim fields (aims version 2): the ten new routes to a national
# seat as fields on the Engine's ladder shapes, with a clock on every rung. Pathways and packs thread, 2026-10-23, for
# v25: Emren's decision #11 (chroma-ideas/next-table-2026-10-19/v25-decisions-emren.md, section 10) and Outer world's
# routes (chroma-world/spheres/data/world_fit.json "national", world-fit-v2.md section 3).
#
# SWITCHED OFF: nothing reads this file until the Engine's aims_v2 is on and `national` is in batch.PACKS (with
# `callings`), so it changes no life.
#
# The format is the Engine's frozen aims shape: chroma-engine/notes/v25/aims-shape.md, sections 3 and 8; other-shapes.md
# section 5 says the routes are aims fields whose top rung is a national seat, so they reuse the aims' clocks, forks and
# assets rather than a quest system of their own. chroma-packs/tools/check_fields.py checks this file (a pack with no
# aims.py has fields of its own).
#
# Each route has five rungs: the route's local step (rung 1, a contribution in town), the trade the route works through
# (rung 2), its Known rung (a name in the field, or the route's own standing), its Notable rung (the "wider" step: the
# asset has spread, or the summit the seat refines; Outer world's climb.who) and the seat at the top (Historic). The
# five entries (local contribution, exceptional work, collaboration, institution-building, wider recognition) are ways
# onto these rungs, so none needs wealth, a city or a single patron; [known across the country] is one name among others
# on a rung, never the only way. The five routes whose seats exist already are v1 aims of other packs (ROUTES below).
#
# Clocks: `years` is (median, 10th, 90th percentile) of steady effort from the rung below, from training lengths and
# the years roles.py asks (each seat after 5 to 15 years at the title it refines); `share` is of those who keep at it,
# the share who reach the rung, so the shares multiply down the ladder; the product at the top (about 2 to 10 in 10,000
# of those who try) was checked against the seats' shares (a few in a million of all people, catalogue.py) and the
# refined titles' shares. Every figure is an estimate unless the comment names a source. `demand` hours are free hours
# a week outside paid work; money and entry are shares of a year's free money. `window` only where the step really has
# outside timing (a yearly intake, a term's appointment), `upkeep` only where a benefit really fades without use; a seat
# has none (its ends are in roles.py). Words a player reads name no real body, paper, bank, park, faith or country.
#
# Dreams: the new modern Earth dreams are in dreams.py (one per route); the tribal and magic ones are the Library's.

FIELDS_NATIONAL = {
    # W, Common-Ground Maker. Clock: ordination or mediation training, 3 to 12 years (callings/fields.py, "to lead a
    # faith"); a senior cleric after 8 years ordained (callings/roles.py); the head of an order from 45, then the seat
    # after 3 years at an order's head or 10 as a senior cleric (roles.py). Sum 18 years to Known, 31 to the top; top
    # .9 x .4 x .25 x .1 x .08.
    "to bring the sides together": dict(
        shape="faith", face="W G", sphere="faith", domain="faith", calling=True,
        dreams=["to bring the feuding sides together", "a lasting peace between the town and the forest folk",
                "an elder whose counsel the clans seek"],
        thing="the peacemaking", doing="bringing the sides together", contest="the councils' choosing",
        places=["faith.congregation", "rule.counsel", "gather.talk"],
        prep=["faith practice", "public speaking", "leading people"], meets=["belonging", "meaning"],
        people=dict(coach="an old minister who settles quarrels over tea",
                    rival="a preacher who takes one side loudly", peer="the others at the mediation evenings",
                    patron="an elder of another faith who asks them to the table"),
        round=["the mediation course at the community centre", "a neighbouring congregation that needs a go-between",
               "the joint service the faiths hold every year"],
        below="{N} is the one who gets both ends of the playground to agree on the rules of the game",
        tribal="to be the peace-weaver every clan's fire welcomes", magic="to be the peace-weaver between the houses",
        rungs=[
            dict(say="a peacemaker close to home", any=["calming people down", "community-mediation volunteer",
                                                        "regular worshipper", "lay religious teacher"],
                 years=(2, 0.5, 5), share=0.9, start=(10, 30, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0, energy=0.2), window=None, upkeep=None),
            # the faiths' colleges and the mediation courses take students once a year; a minister or mediator without
            # a post for years drops off the lists the councils choose from (estimate)
            dict(say="ordained, or a mediator", any=["ordained religious minister", "mediator",
                                                     "member of a monastic community", "mediation accreditation"],
                 years=(6, 3, 12), share=0.4, contests_y=1, forks=["pay", "go_on"],
                 demand=dict(hours=10, money=0.15, entry=0.2, energy=0.5), window=dict(every=1, open_weeks=12),
                 upkeep=dict(of="access", years=5, kept_by=["leading worship", "mediation"])),
            dict(say="trusted by both sides", any=["senior cleric", "standing with both sides",
                                                   "a flock that follows you"],
                 req="was('ordained religious minister') | was('mediator') | was('member of a monastic community')",
                 height="Known", years=(10, 6, 18), share=0.25, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="at the head of an order", any=["head of a faith order"], height="Notable",
                 years=(8, 4, 15), share=0.1, contests_y=0.5, forks=["take", "round"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="the faiths' common voice", any=["head of a national faith body"], height="Historic",
                 years=(5, 3, 12), share=0.08, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
    # U, Discoverer. Clock: a doctorate 3 to 5 years part-time or more (science/fields.py); a research project lead from
    # 27 and a group leader from 30 (science catalogue ages); the chief scientist from 45 after 5 years leading a group
    # or as a professor (roles.py), appointed for a term. Sum 13 years to Known, 27 to the top; top .9 x .45 x .35 x .2
    # x .02.
    "to find what no one knew": dict(
        shape="knowledge", face="U W", sphere="learn", domain="career", calling=True,
        dreams=["to make a discovery known by name", "a scientist", "the one who reads the seasons for the clan",
                "a scholar of the arcane archives"],
        thing="the research", doing="finding things out", contest="the grant round",
        places=["learn.higher", "learn.keeping"], prep=["research", "study", "numbers"],
        meets=["competence", "meaning"],
        people=dict(coach="a supervisor who makes them repeat every result",
                    rival="a group across the country chasing the same question",
                    peer="the others in the reading group", patron="a senior professor who puts their name on a panel"),
        round=["a field station that takes volunteers", "the evening course in data",
               "the yearly meeting where the whole field gathers"],
        below="{N} keeps a notebook of how long the puddle on the path takes to dry, every day for a month",
        tribal="to be the one the gathering asks how the seasons will go", magic="to be first sage of the high college",
        rungs=[
            dict(say="a careful local study", any=["finding things out", "community observer", "research assistant",
                                                   "amateur astronomer in a club"],
                 years=(3, 1, 6), share=0.9, start=(10, 22, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.05, entry=0.05, energy=0.3), window=None, upkeep=None),
            # doctoral places and the first grants come once a year
            dict(say="a result that holds", any=["doctoral graduate", "published research", "research scientist",
                                                 "postdoctoral researcher"],
                 years=(5, 3, 9), share=0.45, contests_y=1, forks=["pay"],
                 demand=dict(hours=12, money=0.3, entry=0.4, energy=0.6), window=dict(every=1, open_weeks=10),
                 upkeep=None),
            # collaborators and the field's attention fade after a few years away from research (estimate)
            dict(say="a name in the field", any=["name in the field", "a finding that held up",
                                                 "research project lead"],
                 req="was('research scientist') | was('postdoctoral researcher') | has('doctoral graduate')",
                 height="Known", years=(5, 2, 10), share=0.35, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=8, money=0.03, entry=0, energy=0.6), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["research", "teaching"])),
            dict(say="a group of your own", any=["research group leader", "professor", "research facility lead"],
                 height="Notable", years=(6, 3, 12), share=0.2, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
            # appointed for a term of about five years (roles.py)
            dict(say="the country's chief scientist", any=["chief scientist"],
                 req="was('professor') | was('research group leader') | was('research facility lead')",
                 height="Historic", years=(8, 4, 18), share=0.02, contests_y=0.2, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=dict(every=5, open_weeks=12),
                 upkeep=None),
        ]),
    # U, Systems Inventor. Clock: a technical trade 2 to 7 years and an inventor after 3 at it (callings/fields.py, "to
    # invent something the world uses"); a celebrated inventor after 5 years as an inventor (callings/roles.py); the
    # laboratory's director from 40 after 5 years leading a facility or 3 as a celebrated inventor (roles.py), for a
    # term of about eight. Sum 14.5 years to Known, 26.5 to the top; top .9 x .35 x .2 x .12 x .04.
    "to build what the country runs on": dict(
        shape="craft", face="U B", sphere="learn", domain="career", calling=True,
        dreams=["to build a system the whole country uses", "an inventor", "a new way of hunting that nobody has tried",
                "to build a flying ship"],
        thing="the system", doing="building things that work", contest="the trial run",
        places=["prod.craft", "learn.higher"], prep=["the craft", "numbers", "research"],
        meets=["competence", "autonomy"],
        people=dict(coach="an old engineer who checks every drawing", rival="a firm racing to build the same thing",
                    peer="the makers at the repair café", patron="a director who gives them a budget and a deadline"),
        round=["the repair café every Saturday", "a maker who needs a partner",
               "the yearly trials where new machines are shown"],
        below="{N} rewires the doorbell so it rings in the kitchen too, and keeps the diagram in a drawer",
        tribal="to be master of the clans' great workings", magic="to be master artificer of the guilds",
        rungs=[
            dict(say="fixing how things run", any=["fixing things", "repair-cafe volunteer", "prototyping",
                                                   "apprentice"],
                 years=(1.5, 0.5, 4), share=0.9, start=(10, 22, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.03, entry=0.03, energy=0.3), window=None, upkeep=None),
            # the maker's hand fades after about five years away from the bench (estimate)
            dict(say="an invention that works", any=["inventor", "a patent of your own", "civil engineer",
                                                     "research software engineer"],
                 years=(6, 3, 12), share=0.35, contests_y=1, forks=["pay", "go_on"],
                 demand=dict(hours=10, money=0.15, entry=0.2, energy=0.55), window=None,
                 upkeep=dict(of="proficiency", years=5, kept_by=["the craft", "work"])),
            dict(say="a system others use", any=["an invention in everyday use", "research facility lead",
                                                 "research project lead"],
                 req="was('inventor') | was('civil engineer') | was('research software engineer') | "
                     "has('a patent of your own')",
                 height="Known", years=(7, 3, 15), share=0.2, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=8, money=0.1, entry=0.1, energy=0.55), window=None, upkeep=None),
            dict(say="a name in the craft", any=["celebrated inventor", "research group leader"], height="Notable",
                 years=(6, 3, 14), share=0.12, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.5), window=None, upkeep=None),
            # the director is appointed for a term of about eight years (roles.py)
            dict(say="the country's great workshop", any=["director of a national laboratory"], height="Historic",
                 years=(6, 3, 14), share=0.04, contests_y=0.2, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=dict(every=8, open_weeks=12),
                 upkeep=None),
        ]),
    # U, Truthfinder. Clock: a journalist from 18 (catalogue ages), most after a degree or a course of 1 to 3 years; the
    # editor of a national paper from 35 after 10 years as a journalist (roles.py). Sum 11 years to Known, 23 to the
    # top; top .9 x .4 x .35 x .12 x .03.
    "to tell the country the truth": dict(
        shape="career", face="U R", sphere="gather", domain="career", calling=True,
        dreams=["to run a great newspaper", "a runner who carries news between the camps", "a storyteller at the fire"],
        thing="the paper", doing="reporting", contest="the story's deadline",
        places=["gather.talk", "arts.page", "rule.voice"], prep=["writing", "research", "reading"],
        meets=["meaning", "autonomy"],
        people=dict(coach="a night editor who cuts every sentence that was not checked",
                    rival="a reporter at the other paper chasing the same story", peer="the newsroom",
                    patron="an owner who backs the story when the lawyers call"),
        round=["the town's free sheet, which takes anyone who can write", "the community radio's news hour",
               "the evening course in reporting, every week"],
        below="{N} writes a one-page news sheet of the street, with a box for corrections on the back",
        tribal="to be the keeper of the clans' telling", magic="to be chronicler of the realm",
        rungs=[
            dict(say="reporting a local wrong", any=["reporting", "community-radio presenter", "writing stories",
                                                     "finding things out"],
                 years=(2, 0.5, 5), share=0.9, start=(12, 24, 35), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            # contacts and sources go cold after a few years out of the news (estimate)
            dict(say="a reporter", any=["journalist"], years=(3, 1, 6), share=0.4, contests_y=0,
                 forks=["pay", "take"], demand=dict(hours=10, money=0.15, entry=0.25, energy=0.55), window=None,
                 upkeep=dict(of="access", years=3, kept_by=["work", "writing"])),
            dict(say="sources who trust you", any=["source who trusts you", "name in the field"],
                 req="was('journalist')", height="Known", years=(6, 3, 12), share=0.35, contests_y=1,
                 forks=["round", "take"], demand=dict(hours=8, money=0.02, entry=0, energy=0.6), window=None,
                 upkeep=None),
            dict(say="read across the country", any=["known across the country"], req="was('journalist')",
                 height="Notable", years=(6, 3, 14), share=0.12, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="the paper the country reads", any=["editor of a national paper"], height="Historic",
                 years=(6, 3, 14), share=0.03, contests_y=0.5, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.7), window=None, upkeep=None),
        ]),
    # B, Coalition Builder. Clock: a business of one's own 3 to 20 years from a head for a deal (callings/fields.py, "to
    # build an empire"); a chief executive from 28 after 3 years as a founder (callings/roles.py); the industry body's
    # head from 40 after 5 years as a chief executive or 10 as a founder (roles.py), elected by the members every few
    # years. Sum 15.5 years to Known, 26.5 to the top; top .9 x .45 x .2 x .15 x .05.
    "to make a whole industry move together": dict(
        shape="career", face="B U", sphere="prod", domain="career", calling=True,
        dreams=["to speak for a whole industry", "a trader between the clans", "a master of one's guild"],
        thing="the alliance", doing="bringing the firms together", contest="the members' vote",
        places=["comm.market", "rule.counsel", "gather.great"], prep=["the market", "organising", "leading people"],
        meets=["competence", "belonging"],
        people=dict(coach="a retired chair who knows every grudge in the trade",
                    rival="a firm that would rather go it alone", peer="the other owners at the trade dinners",
                    patron="a minister's adviser who wants one voice to talk to"),
        round=["the town's traders' association", "a rival who might partner on one contract",
               "the trade fair every spring"],
        below="{N} gets the three lemonade stands on the street to share one big sign",
        tribal="to bind the clans' traders and hunters to one hunting law", magic="to be kingmaker of the houses",
        rungs=[
            dict(say="a head for a deal", any=["striking a deal", "selling", "club treasurer", "shop assistant"],
                 years=(1.5, 0.5, 4), share=0.9, start=(12, 25, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.3), window=None, upkeep=None),
            dict(say="a firm of your own", any=["founder of a firm", "shop owner", "shift manager"],
                 years=(6, 3, 12), share=0.45, contests_y=0, forks=["pay", "take"],
                 demand=dict(hours=12, money=0.2, entry=0.4, energy=0.65), window=None, upkeep=None),
            # backers and boards drift to others after a few years out of business (estimate)
            dict(say="at the head of a large firm", any=["chief executive", "investors who back you"],
                 req="was('founder of a firm') | was('shop owner') | was('shift manager')", height="Known",
                 years=(8, 3, 15), share=0.2, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=8, money=0.05, entry=0.05, energy=0.65), window=None,
                 upkeep=dict(of="access", years=4, kept_by=["work", "boards"])),
            dict(say="the rivals at one table", any=["a seat on boards", "magnate", "celebrated inventor"],
                 height="Notable", years=(5, 2, 10), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.03, entry=0, energy=0.6), window=None, upkeep=None),
            # the members elect the head every few years (estimate)
            dict(say="the voice of a whole industry", any=["head of a national industry body"], height="Historic",
                 years=(6, 3, 12), share=0.05, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=dict(every=3, open_weeks=8),
                 upkeep=None),
        ]),
    # B, Opportunity Patron. Clock: an accountant from 21 after a degree and a professional course of about 3 years; the
    # bank's head from 40 after 5 years as a chief executive or 15 as an accountant (roles.py), appointed for a term.
    # Sum 15 years to Known, 27 to the top; top .9 x .4 x .2 x .15 x .02.
    "to back the ones who will matter": dict(
        shape="career", face="B U", sphere="comm", domain="career", calling=True,
        dreams=["to back the people nobody else will", "to be owed a favour in every camp", "a merchant prince"],
        thing="the fund", doing="backing ventures", contest="the board's vote",
        places=["comm.credit", "comm.market"], prep=["numbers", "the market"], meets=["competence", "autonomy"],
        people=dict(coach="an old banker who taught them to read people, not only figures",
                    rival="a fund that wants the same deals", peer="the others on the lending panel",
                    patron="a backer who staked them early"),
        round=["the town's credit union, which needs a treasurer", "a small venture nobody else will back",
               "the yearly evening where new firms ask for money"],
        below="{N} lends a friend the bus fare and writes the date in a little book, and is always paid back",
        tribal="to keep the gathering's gift-stores and decide which clan is lent seed",
        magic="to be patron of the realm's ventures",
        rungs=[
            dict(say="a head for numbers", any=["bookkeeping", "club treasurer", "office clerk"],
                 years=(2, 0.5, 5), share=0.9, start=(12, 25, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=3, money=0.02, entry=0.02, energy=0.25), window=None, upkeep=None),
            # an accountant's registration lapses after years out of practice (estimate)
            dict(say="a career in money", any=["accountant", "founder of a firm"], years=(5, 3, 10), share=0.4,
                 contests_y=1, forks=["pay"], demand=dict(hours=10, money=0.2, entry=0.3, energy=0.55), window=None,
                 upkeep=dict(of="credential", years=5, kept_by=["work"])),
            dict(say="money that works", any=["investors who back you", "chief executive", "shares"],
                 req="was('accountant') | was('founder of a firm')", height="Known", years=(8, 4, 15), share=0.2,
                 contests_y=1, forks=["take", "round"], demand=dict(hours=6, money=0.1, entry=0.1, energy=0.55),
                 window=None, upkeep=None),
            dict(say="a backer people seek out", any=["a seat on boards", "a portfolio of people backed"],
                 height="Notable", years=(6, 3, 12), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.55), window=None, upkeep=None),
            # appointed by the board or the government for a term of about seven years (roles.py)
            dict(say="the country's money", any=["head of a national bank or exchange"], height="Historic",
                 years=(6, 3, 12), share=0.02, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.65), window=dict(every=7, open_weeks=12),
                 upkeep=None),
        ]),
    # R, National Virtuoso. Clock: drama school or a club's academy 2 to 8 years (stage/fields.py, "to be a star"); the
    # star after 5 years as a lead or a touring musician, or 4 as a professional athlete (roles.py). A professional
    # athlete's ages end at 40 (catalogue), so the road through sport is short. Sum 9 years to Known, 17 to the top;
    # top .9 x .2 x .35 x .15 x .1.
    "to perform for the whole country": dict(
        shape="art", face="R B", sphere="arts", domain="career", calling=True,
        dreams=["to perform before the whole country", "to be famous", "a star footballer",
                "the champion wrestler of the gatherings", "a name sung in every tavern"],
        thing="the performance", doing="performing", contest="the big night",
        places=["arts.stage", "gather.games", "arts.song"], prep=["performing", "fitness", "music"],
        meets=["competence", "meaning"],
        people=dict(coach="a coach who films every performance and plays it back",
                    rival="a rival with more natural talent", peer="the company or the team",
                    patron="an agent who gets them the first big booking"),
        round=["the local club or company, which takes anyone who turns up", "a second try at the trials next year",
               "the summer festival every year"],
        below="{N} puts on a show in the garden for anyone who will sit still, with tickets drawn in crayon",
        tribal="to be the singer or champion every clan knows", magic="to be bard or champion of the realm",
        rungs=[
            dict(say="the local stage or field", any=["amateur actor", "on the team", "amateur band member",
                                                      "team captain"],
                 years=(2, 0.5, 5), share=0.9, start=(6, 16, 25), contests_y=0, forks=["go_on"],
                 demand=dict(hours=5, money=0.03, entry=0.02, energy=0.45), window=None, upkeep=None),
            # auditions and trials come once a year; form fades after about two years without training or performing
            dict(say="a professional", any=["professional athlete", "touring musician", "professional actor"],
                 years=(4, 2, 8), share=0.2, contests_y=1, forks=["pay", "take"],
                 demand=dict(hours=12, money=0.15, entry=0.2, energy=0.7), window=dict(every=1, open_weeks=6),
                 upkeep=dict(of="proficiency", years=2, kept_by=["training", "performing"])),
            dict(say="a performance people talk of", any=["a lead role to remember", "lead actor or actress",
                                                          "a known face"],
                 req="was('professional athlete') | was('touring musician') | was('professional actor')",
                 height="Known", years=(3, 1, 8), share=0.35, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=8, money=0.05, entry=0, energy=0.7), window=None, upkeep=None),
            dict(say="known across the country", any=["known across the country", "a household name"],
                 height="Notable", years=(4, 2, 10), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.6), window=None, upkeep=None),
            dict(say="a star of the whole country", any=["celebrated star of stage or sport"], height="Historic",
                 years=(4, 2, 10), share=0.1, contests_y=1, forks=["take"],
                 demand=dict(hours=6, money=0.05, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
    # G, Living-Land Steward. Clock: a ranger or forester from 18 to 20 after a course of 1 to 3 years (catalogue ages);
    # the head of the national parks from 35 after 10 years as a ranger or forester (roles.py), appointed for a term of
    # about eight. Sum 11 years to Known, 25 to the top; top .9 x .3 x .4 x .2 x .03.
    "to keep the country's wild places": dict(
        shape="career", face="G U", sphere="prod", domain="career", calling=True,
        dreams=["to keep the wild places for everyone", "a ranger of the borderlands", "a keeper of the old grove",
                "a gatherer who knows every plant"],
        thing="the reserve", doing="keeping the land", contest="the planning hearing",
        places=["prod.wild", "prod.land", "rule.counsel"], prep=["the land", "organising", "research"],
        meets=["meaning", "competence"],
        people=dict(coach="an old ranger who knows where every badger sett is",
                    rival="a developer who wants the valley", peer="the volunteers on the Sunday work parties",
                    patron="a farmer who lends a field to try it on"),
        round=["the Sunday work party on the common", "a farmer who will try it on one field",
               "the yearly count of the birds and the flowers"],
        below="{N} builds a little fence of sticks round the frog spawn in the ditch and checks it every morning",
        tribal="to be warden of the valley's wild places", magic="to be a druid of the circle, warden of the wilds",
        rungs=[
            dict(say="a local stretch tended", any=["community-garden coordinator", "gardener or groundskeeper",
                                                    "community observer"],
                 years=(2, 0.5, 5), share=0.9, start=(10, 25, 40), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.02, entry=0.02, energy=0.4), window=None, upkeep=None),
            # the services take new rangers and foresters once a year
            dict(say="a keeper of the land by trade", any=["park ranger", "forester"], years=(3, 1, 6), share=0.3,
                 contests_y=1, forks=["pay", "take"], demand=dict(hours=10, money=0.1, entry=0.2, energy=0.6),
                 window=dict(every=1, open_weeks=8), upkeep=None),
            dict(say="a name for the place", any=["good name in town", "community partners"],
                 req="was('park ranger') | was('forester')", height="Known", years=(6, 3, 12), share=0.4,
                 contests_y=1, forks=["round", "take"], demand=dict(hours=6, money=0.02, entry=0, energy=0.55),
                 window=None, upkeep=None),
            dict(say="a stretch kept alive", any=["a stretch of land kept alive"], height="Notable", years=(6, 3, 12),
                 share=0.2, contests_y=1, forks=["take"], demand=dict(hours=6, money=0.02, entry=0, energy=0.55),
                 window=None, upkeep=None),
            # appointed for a term of about eight years (roles.py)
            dict(say="the country's wild places", any=["head of the national parks"], height="Historic",
                 years=(8, 4, 16), share=0.03, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=dict(every=8, open_weeks=12),
                 upkeep=None),
        ]),
    # G, Living-Heritage Keeper. Clock: a curator or archivist from 22 to 23 after a degree and a further course; a
    # master craftsperson from 30 (art catalogue ages); the keeper from 40 after 10 years as a curator, archivist or
    # master, or 15 as a folk musician (roles.py). Sum 17 years to Known, 31 to the top; top .9 x .35 x .3 x .15 x .04.
    "to keep the old ways alive": dict(
        shape="cause", face="G R", sphere="arts", domain="community", calling=True,
        dreams=["to keep the old songs and crafts alive", "to know what the old stories really mean",
                "to know more songs than anyone"],
        thing="the tradition", doing="keeping the old ways", contest="the heritage panel",
        places=["arts.craft", "arts.song", "learn.keeping"], prep=["the craft", "music", "research"],
        meets=["belonging", "meaning"],
        people=dict(coach="an old fiddler or weaver who teaches it the way it was taught to them",
                    rival="a museum that wants every piece behind glass", peer="the others at the folk club",
                    patron="a trust that pays for the workshop"),
        round=["the folk club every Thursday", "a festival that needs someone to run the craft tent",
               "the village's yearly custom, which needs a new keeper"],
        below="{N} learns every verse of a grandparent's old song and writes them down before anyone forgets",
        tribal="to be the lorekeeper of the gathering", magic="to be lorekeeper of the realm",
        rungs=[
            dict(say="keeping a local custom", any=["folk musician", "craft maker", "festival organiser",
                                                    "archive research"],
                 years=(3, 1, 8), share=0.9, start=(10, 25, 45), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.03, entry=0.03, energy=0.3), window=None, upkeep=None),
            dict(say="a keeper by trade or by hand", any=["museum curator", "archivist", "professional conservator",
                                                          "a maker's hallmark"],
                 years=(6, 3, 12), share=0.35, contests_y=0, forks=["pay", "go_on"],
                 demand=dict(hours=8, money=0.1, entry=0.2, energy=0.45), window=None, upkeep=None),
            dict(say="a master of the old ways", any=["master craftsperson", "name in the field"],
                 req="was('folk musician') | was('craft maker') | was('museum curator') | was('archivist') | "
                     "was('professional conservator')",
                 height="Known", years=(8, 4, 15), share=0.3, contests_y=1, forks=["take", "round"],
                 demand=dict(hours=6, money=0.03, entry=0, energy=0.45), window=None, upkeep=None),
            dict(say="a living tradition kept", any=["a living tradition kept", "known across the country"],
                 height="Notable", years=(8, 4, 18), share=0.15, contests_y=1, forks=["take"],
                 demand=dict(hours=5, money=0.02, entry=0, energy=0.4), window=None, upkeep=None),
            dict(say="what the country remembers", any=["keeper of the national heritage"], height="Historic",
                 years=(6, 3, 14), share=0.04, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.5), window=None, upkeep=None),
        ]),
    # G, Community Weaver. Clock: a community centre manager from 21 (catalogue ages) after years of running groups;
    # the national charity's head from 35 after 8 years as a manager, 10 as a garden coordinator or 3 as a renowned
    # healer (roles.py). Sum 12 years to Known, 26 to the top; top .9 x .4 x .45 x .12 x .05.
    "to join the helpers of every town": dict(
        shape="cause", face="G W", sphere="care", domain="community", calling=True,
        dreams=["to link the helpers of every town", "a grandmother or grandfather to the whole camp",
                "to keep the band together through the hard seasons"],
        thing="the network", doing="helping the town help itself", contest="the trustees' meeting",
        places=["gather.hall", "care.houses", "gather.circle"], prep=["organising", "care", "leading people"],
        meets=["belonging", "meaning"],
        people=dict(coach="an old organiser who has run the food bank for thirty years",
                    rival="a big charity that wants to take the local group over", peer="the volunteers' rota",
                    patron="a trust officer who funds the first year"),
        round=["the community kitchen's rota every week", "a group in the next town with the same trouble",
               "the yearly gathering of all the groups"],
        below="{N} organises the street's children into a rota to walk the old neighbour's dog",
        tribal="to be the hearth-mother or hearth-father of the clans",
        magic="to be warden of the realm's almshouses and mutual guilds",
        rungs=[
            dict(say="a neighbourhood group", any=["community-kitchen volunteer", "hospice volunteer",
                                                   "parent-association organiser", "organising people"],
                 years=(2, 0.5, 5), share=0.9, start=(12, 30, 50), contests_y=0, forks=["go_on"],
                 demand=dict(hours=4, money=0.01, entry=0, energy=0.3), window=None, upkeep=None),
            dict(say="running something that holds", any=["community centre manager", "community-garden coordinator",
                                                          "festival organiser"],
                 years=(5, 2, 10), share=0.4, contests_y=0, forks=["go_on", "take"],
                 demand=dict(hours=8, money=0.02, entry=0.02, energy=0.5), window=None, upkeep=None),
            dict(say="the town's own", any=["good name in town", "community partners"],
                 req="was('community centre manager') | was('community-garden coordinator')", height="Known",
                 years=(5, 2, 10), share=0.45, contests_y=1, forks=["round", "take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="a web of groups", any=["a web of groups that help each other", "known across the country"],
                 height="Notable", years=(8, 4, 16), share=0.12, contests_y=1, forks=["take"],
                 demand=dict(hours=8, money=0.02, entry=0, energy=0.55), window=None, upkeep=None),
            dict(say="the helpers of the whole country", any=["head of a national charity"], height="Historic",
                 years=(6, 3, 12), share=0.05, contests_y=0.5, forks=["take"],
                 demand=dict(hours=6, money=0.02, entry=0, energy=0.6), window=None, upkeep=None),
        ]),
}

# The fifteen routes (world_fit.json "national", routes) and the aim each runs through. The five seats that exist are
# the tops of other packs' v1 aims, whose own fields are in those packs' fields.py; the Engine's climb reads the route
# of an aim from this map (aim_x: an aim's next rung is a standing-3 title).
ROUTES = {
    "mandate_builder": "to lead the country",                          # politics: head of government
    "public_service_architect": "to be the one who makes things happen",   # politics: minister
    "common_ground_maker": "to bring the sides together",
    "discoverer": "to find what no one knew",
    "systems_inventor": "to build what the country runs on",
    "truthfinder": "to tell the country the truth",
    "enterprise_builder": "to build an empire",                        # callings: magnate
    "coalition_builder": "to make a whole industry move together",
    "opportunity_patron": "to back the ones who will matter",
    "rallying_voice": "to build a movement",                           # politics: party leader
    "national_virtuoso": "to perform for the whole country",
    "commander": "to command an army",                                 # callings: general
    "living_land_steward": "to keep the country's wild places",
    "living_heritage_keeper": "to keep the old ways alive",
    "community_weaver": "to join the helpers of every town",
}
