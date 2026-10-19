# Chroma content pack: The Five Callings. The pack in the other worlds.
# Pathways and packs thread, 2026-10-19, in the shape of ../art/worlds.py, after Emren (10-05 21:37): modern world
# conditions and terms first, "but dont forget that applications must be feasible for other wordly setting, even
# including supernatural sometimes", and the grand objective (10-19 08:53): the colour pie is the backbone of fantasy
# realms with magic, gods, kingdoms and cosmology. The catalogue stays in modern Earth terms; this file gives each title
# and perk its form in the game's tribal and magic worlds (chroma-game/prototype/story.py, SETTINGS and WORLD), so each
# road keeps the same shape everywhere: the same rungs, doors, steps and falls. Plain data for the Library and the
# game; nothing runs.
#
# The shape of the five callings in each world (the Vision thread's faces, 10-19 12:04):
#   earth   congregations, seminaries and faith bodies; workshops, patents and the firms that make things; shops,
#           firms, boards and business groups; the army's ranks, the academy and the general staff; wards, birth
#           centres, district rounds and clinics.
#   tribal  the keeper of the rites and the great shaman; the toolmaker whose new ways spread from band to band; the
#           trader owed a favour in every camp; the leader of the hunters and the guard, and the war leader of the
#           clans; the birth-keeper and the healer every band sends for, who knows every plant.
#   magic   a priest of a god's temple and the high priest of the order; the artificer and the realm's maker of
#           wonders; the guild master and the merchant prince; a captain of the realm's army and the warlord or
#           general; the herb-healer of the temple house and the druid-healer known across the realm.
#
# Supernatural ways are possible sometimes and never forced: world-only moments (in each road's .lib file), each
# optional, each with a price, and never resting on the person's own gift (round 5's rule): an oracle's word, an
# enchanter's binding, a spirit's bargain. Modern Earth has no magic.
#
# Fields: tribal and magic, the form in that world; note, how it maps: "same rung" when the role exists as it is,
# "nearest" when a stand-in keeps the road's shape.

WORLDS_CALLINGS = {
    # ------------------------------------------------ W: the faith leader
    "senior cleric": dict(tribal="a keeper of the rites for many bands", magic="a priest of a great temple",
                          note="same rung"),
    "head of a faith order": dict(tribal="the great shaman whom every band heeds",
                                  magic="high priest of a god's order", note="same rung"),
    # ------------------------------------------------ U: the inventor
    "inventor": dict(tribal="the toolmaker whose new ways spread from band to band", magic="an artificer",
                     note="same rung"),
    "celebrated inventor": dict(tribal="the maker whose boat first crossed the great lake",
                                magic="the realm's artificer, maker of wonders", note="same rung"),
    # ------------------------------------------------ B: the magnate
    "chief executive": dict(tribal="the trader who runs a band's trade at the gatherings", magic="a guild master",
                            note="same rung"),
    "magnate": dict(tribal="the trader owed a favour in every camp", magic="a merchant prince", note="same rung"),
    # ------------------------------------------------ R: the commander
    "army officer": dict(tribal="a leader of the hunters and the guard", magic="a captain of the realm's army",
                         note="same rung"),
    "general": dict(tribal="the war leader of the clans", magic="a warlord, general of the realm", note="same rung"),
    # ------------------------------------------------ G: the healer
    "senior nurse or midwife": dict(tribal="the band's birth-keeper and first healer",
                                    magic="a healer of the temple house", note="same rung"),
    "renowned healer": dict(tribal="the healer every band sends for, who knows every plant",
                            magic="a herb-healer or druid-healer known across the realm", note="same rung"),
    # ------------------------------------------------ base titles the roads use
    "ordained religious minister": dict(tribal="one who leads the band's rites", magic="a priest", note="same rung"),
    "member of a monastic community": dict(tribal="one who lives apart at the sacred place",
                                           magic="a monk or nun of an order", note="same rung"),
    "founder of a firm": dict(tribal="one who starts a trade of their own between the bands",
                              magic="a merchant with a house of their own", note="same rung"),
    "soldier": dict(tribal="a hunter of the guard", magic="a soldier of the realm", note="same rung"),
    # ------------------------------------------------ perks
    "leading soldiers": dict(tribal="leading the guard", magic="leading soldiers", note="same"),
    "preaching": dict(tribal="speaking for the spirits at the fire", magic="preaching", note="same"),
    "prototyping": dict(tribal="making a new tool and trying it", magic="building a working model", note="same"),
    "a degree in theology": dict(tribal="the old shaman's years of teaching", magic="the temple school's seal",
                                 note="tribal: nearest"),
    "an officer's commission": dict(tribal="the elders' leave to lead the guard", magic="a captain's commission",
                                    note="same"),
    "licence to prescribe": dict(tribal="the leave to give the strong plants", magic="the apothecaries' licence",
                                 note="tribal: nearest"),
    "an invention in everyday use": dict(tribal="a tool every band now makes", magic="a device in every household",
                                         note="same"),
    "a seat on boards": dict(tribal="a voice at every trading circle", magic="a seat on the guild councils",
                             note="same"),
    "mentioned in dispatches": dict(tribal="named for courage at the fire", magic="named in the captain's report",
                                    note="same"),
    "families who send for you": dict(tribal="families who send for you", magic="families who send for you",
                                      note="same"),
    "a flock that follows you": dict(tribal="followers who would move camp with you",
                                     magic="a congregation that follows you", note="same"),
    "investors who back you": dict(tribal="traders who share their goods with you",
                                   magic="backers among the merchant houses", note="same"),
    "a business empire": dict(tribal="trade in every camp along the rivers", magic="a merchant house of many halls",
                              note="same"),
    "a patent of your own": dict(tribal="a tool only you may make", magic="the guild's grant on a design",
                                 note="tribal: nearest"),
    "a clinic of your own": dict(tribal="a healer's lodge of your own", magic="a house of healing of your own",
                                 note="same"),
}

# World-only moments, each optional and each with a price (written in the road's own .lib file).
WORLD_ONLY_CALLINGS = {
    "the god speaks in the temple": dict(only="magic", kind="crossing",
                                         what="an oracle says the god has chosen a new high priest; the priest who "
                                              "listens may be named, at a price the oracle names"),
    "the guild commissions a flying ship": dict(only="magic", kind="crossing",
                                                what="the artificers' guild wants a ship that flies; an enchanter's "
                                                     "binding can make it rise, with the Order's leave"),
    "a seat among the merchant princes": dict(only="magic", kind="crossing",
                                              what="a seat on the council of merchant princes falls free; a "
                                                   "bargain with something old can buy the votes"),
    "the war leader is chosen at the gathering": dict(only="tribal", kind="crossing",
                                                      what="the clans gather to choose who leads them if raiders "
                                                           "come; the elders and the spirits both have a say"),
    "the sickness in the winter camp": dict(only="tribal", kind="crossing",
                                            what="a fever runs through the winter camp; the healer who stays and "
                                                 "nurses every tent becomes the one every band sends for"),
}
