# ---------- volume 2, asset: what the person owns; when it is gone it is gone (skill_half None)
PERKS += [
  dict(name="hives of one's own", kind="asset", ways="G U", odds=0, skill_half=None, retires=None,
       ages=(14, 100), share=.005,   # estimate: the EU counts about 600,000 beekeepers (European Commission), and many
                                     # give up after a few seasons
       say="has hives of their own",
       gained="a course with the local beekeepers and a swarm caught in a box, kept on a [plot of land], a farm or "
              "an allotment; a [professional beekeeper] grows from here",
       lost="'a third of the hives dead after winter' and not started again; a move with nowhere to keep them; old "
            "age and heavy boxes",
       needs="a garden, a [plot of land] or a farmer's corner where they may stand; neighbours who do not mind"),
  dict(name="boat of one's own", kind="asset", ways="R G", odds=0, skill_half=None, retires=None,
       ages=(16, 100), share=.08,   # estimate: about 1 US household in 10 owns a boat (NMMA); Sweden counts close to
                                    # 900,000 leisure boats for 10 million people; far fewer in Britain
       say="has a boat of their own",
       gained="a second-hand dinghy, a fishing boat on a trailer or a narrowboat bought with [savings] after "
              "summers of [boat handling] or [hunting and fishing]",
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
