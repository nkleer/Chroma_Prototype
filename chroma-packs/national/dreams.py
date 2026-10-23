# Chroma content pack: National standing. Dreams for the ten new routes (Pathways and packs thread, 2026-10-23, for
# v25), for the Library's dreams.py, in the same fields as chroma-packs/core/dreams.py.
#
# SWITCHED OFF: the engine never reads this file; it is the source. The Library has copied the ten into its dreams.py
# as DREAMS_NATIONAL, DREAM_KIND_NATIONAL and TRIGGER_NATIONAL (feature/v25 af2c1a0, wording unchanged), which the
# Engine reads only with wa_nat_climb on. check_fields.py reads this file for the names the fields use.
#
# Why: a dream is how a life left alone takes up an aim (68% of the aims taken on head 10 came from dreams), and no
# modern Earth dream points at the ten new seats' routes. One dream per route in modern Earth; the tribal and magic
# worlds already have dreams near each route's realm reading (a ranger of the borderlands, a merchant prince, an elder
# whose counsel the clans seek), which the fields name beside these.
#
# Colour balance: each dream's means is a pair at .5 each, and the ten together give every colour 2.0 (W U B R G), so
# the Library's colour-even rule per world holds for the set; adding only some of them breaks it. The pairs follow the
# seats' ways, except two: the industry body's dream leans B R (the rivals brought to one table) and the bank's B W
# (standing by those backed), so that each colour leads two dreams. Every name is new to dreams.py and to the packs'
# core/dreams.py, and none names a real place, year or brand.

DREAMS_PACKS = [
  dict(name="to bring the feuding sides together", means="W.5 G.5", domain="faith", stages="young_adult adult mature",
       worlds="earth", passion="making peace", plan="learn to listen to both sides, and be trusted by each",
       life="a quarrel of generations settled, with both sides at the table"),
  dict(name="to make a discovery known by name", means="U.5 W.5", domain="career", stages="juvenile young_adult adult",
       worlds="earth", passion="finding things out", plan="study, test every result twice, and publish what holds",
       life="a finding the whole country relies on"),
  dict(name="to build a system the whole country uses", means="U.5 B.5", domain="career",
       stages="juvenile young_adult adult", worlds="earth", passion="making things work",
       plan="learn a technical trade, then build something bigger than one machine",
       life="a working system in every town"),
  dict(name="to run a great newspaper", means="U.5 R.5", domain="career", stages="juvenile young_adult adult",
       worlds="earth", passion="the news", plan="report the town's wrongs, and check every word",
       life="a paper the whole country trusts"),
  dict(name="to speak for a whole industry", means="B.5 R.5", domain="career", stages="young_adult adult mature",
       worlds="earth", passion="business and bargaining", plan="build a firm, then bring the rivals to one table",
       life="a whole trade that moves together"),
  dict(name="to back the people nobody else will", means="B.5 W.5", domain="career",
       stages="young_adult adult mature", worlds="earth", passion="money and people",
       plan="learn to read a venture and its people, then stake them", life="names everyone knows, backed early"),
  dict(name="to perform before the whole country", means="R.5 B.5", domain="career", stages="child juvenile young_adult",
       worlds="earth", passion="performing", plan="train every day and take every stage or field there is",
       life="a performance the whole country remembers"),
  dict(name="to keep the wild places for everyone", means="G.5 U.5", domain="career",
       stages="child juvenile young_adult adult", worlds="earth", passion="the wild",
       plan="learn the land, work as a ranger, and win its keepers over",
       life="a valley or a coast kept alive for good"),
  dict(name="to keep the old songs and crafts alive", means="G.5 R.5", domain="community",
       stages="juvenile young_adult adult mature", worlds="earth", passion="the old ways",
       plan="learn them from the last who know, and teach them on", life="a tradition the young still keep"),
  dict(name="to link the helpers of every town", means="G.5 W.5", domain="community",
       stages="young_adult adult mature", worlds="earth", passion="helping",
       plan="run one group well, then join it to the others", life="groups in every town that help each other"),
]

DREAM_KIND_PACKS = {
  "to bring the feuding sides together": "own", "to make a discovery known by name": "own",
  "to build a system the whole country uses": "own", "to run a great newspaper": "status",
  "to speak for a whole industry": "status", "to back the people nobody else will": "status",
  "to perform before the whole country": "play", "to keep the wild places for everyone": "play",
  "to keep the old songs and crafts alive": "own", "to link the helpers of every town": "own",
}

# Suggested sparks (TRIGGER_DREAMS["earth"][spark] gains these names); only sparks dreams.py already has.
TRIGGER_MORE = {
  "earth": {
    "a street protest": ("to run a great newspaper", "to bring the feuding sides together",
                         "to link the helpers of every town"),
    "a rags-to-riches story": ("to speak for a whole industry", "to back the people nobody else will"),
    "a nature documentary": ("to keep the wild places for everyone",),
    "a parade or a festival": ("to keep the old songs and crafts alive",),
    "a match or a contest": ("to perform before the whole country",),
    "a teacher or coach": ("to make a discovery known by name",),
    "a neighbour's workshop in the shed": ("to build a system the whole country uses",),
  },
}
