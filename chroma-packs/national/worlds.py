# Chroma content pack: National standing. The pack in the other worlds. The catalogue stays in modern Earth terms;
# this file gives each seat and route asset its form in the game's tribal and magic worlds (chroma-game/prototype/
# story.py, SETTINGS and WORLD), so each route keeps the same shape everywhere: the same rungs, the same asset and
# obligation, the same ends. Plain data for the Library and the game; nothing runs.
#
# SWITCHED OFF: nothing reads this file until the Engine adds `national` to batch.PACKS.
#
# National is the realm's widest ring (Outer world's world_fit.json "national", realm): in the tribal world the moot of
# all the clans of a valley at the summer gathering; in the magic world the realm's court, its Assembly and the great
# Orders and guilds. Each route's `realm` in world_fit.json says how it reads there (a peace-weaver between houses, a
# sage of the high college, a druid of the circle), and the forms below follow it. A seat in the tribal world is held
# by acclaim at the gathering and kept while the clans still send for the holder; in the magic world it is held by
# warrant of the throne, an Order or a guild. Supernatural ways in and out are possible sometimes and never forced: the
# Library's route encounters may carry world-only options, each with a price. Modern Earth has no magic.
#
# Fields: tribal and magic, the form in that world (a plain phrase the story can use); note, how it maps: "same rung"
# when the role exists as it is, "nearest" when the role cannot exist there and a stand-in keeps the route's shape.

WORLDS_NATIONAL = {
    # ------------------------------------------------ the seats
    "head of a national faith body": dict(
        tribal="the eldest of the shamans, who keeps the peace between the clans' spirits at the gathering",
        magic="the peace-weaver of the realm's temples, high priest or priestess of the faiths' common council",
        note="same rung; the route reads as a peace-weaver between houses"),
    "chief scientist": dict(
        tribal="the one the gathering asks how the herds, the rivers and the seasons will go",
        magic="first sage of the high college, who counsels the throne on what is known",
        note="tribal: nearest (no science; the knowing of the land and the sky); magic: same rung"),
    "director of a national laboratory": dict(
        tribal="master of the great workings: the fish weirs, the ways across the marsh, the stores",
        magic="master artificer of the guilds' great workshop, where the realm's engines are made",
        note="tribal: nearest (no laboratories; the shared works of the clans); magic: same rung"),
    "editor of a national paper": dict(
        tribal="the keeper of the clans' telling, whose account of a season is the one the fires repeat",
        magic="chronicler of the realm, whose broadsheet and annals the whole kingdom reads",
        note="tribal: nearest (no writing; the telling); magic: same rung"),
    "head of a national industry body": dict(
        tribal="the one who binds the clans' traders, flint-knappers and hunters to share the hunting grounds",
        magic="kingmaker of the great houses: master of the guild of guilds",
        note="tribal: nearest (no industry; the clans' crafts together); magic: same rung"),
    "head of a national bank or exchange": dict(
        tribal="keeper of the gift-stores of the gathering, who decides which clan is lent seed and stock",
        magic="patron of the realm's ventures: master of the royal exchange and its counting houses",
        note="tribal: nearest (no money; stores and gifts); magic: same rung"),
    "celebrated star of stage or sport": dict(
        tribal="the singer or champion of the gathering, whose songs and feats every clan knows",
        magic="bard or champion of the realm, called to sing or fight before the throne",
        note="same rung"),
    "head of the national parks": dict(
        tribal="the warden of the valley's wild places, whom the clans ask before a forest is burned or a river "
               "dammed",
        magic="a druid of the circle, warden of the realm's wilds by charter of the throne",
        note="same rung; the Living-Land Steward reads as a druid of the circle or a warden of the wilds"),
    "keeper of the national heritage": dict(
        tribal="the lorekeeper of the gathering, who knows every clan's songs, crafts and sacred places",
        magic="lorekeeper of the realm, keeper of its archive, its relic halls and its old crafts",
        note="same rung"),
    "head of a national charity": dict(
        tribal="the hearth-mother or hearth-father of the clans, who sees that no camp goes hungry in a hard winter",
        magic="warden of the realm's almshouses and mutual guilds, who keeps each town's own way while they help "
              "each other",
        note="same rung; the route reads as a hearth-mother of the clans"),
    # ------------------------------------------------ the route assets
    "a standing mandate": dict(tribal="the gathering's acclaim for what was promised at the fire",
                               magic="the Assembly's charter for what was promised", note="same"),
    "a working public service": dict(tribal="the clans' granaries and their keepers, which every camp relies on",
                                     magic="a service of the Crown that runs in every town: the granaries, the roads",
                                     note="same; the route reads as the steward of a kingdom's granaries"),
    "standing with both sides": dict(tribal="welcome at every clan's fire, even the feuding ones",
                                     magic="welcome in every house, even the warring ones", note="same"),
    "a finding and its method": dict(tribal="a knowing of the land that held, and the way it was learned",
                                     magic="a finding of the high college and its proof", note="same"),
    "a working national system": dict(tribal="a working the clans all use: the weirs, the marsh path",
                                      magic="an engine or a warding the whole realm uses", note="same"),
    "a record and its sources": dict(tribal="a telling the fires trust, and the witnesses behind it",
                                     magic="a chronicle the realm trusts, and the witnesses behind it", note="same"),
    "the voice of a whole industry": dict(tribal="the voice of every trader and hunter of the valley",
                                          magic="the voice of every guild of the realm", note="same"),
    "a firm and its people": dict(tribal="a trading band and its families", magic="a merchant house and its people",
                                  note="same; the route reads as a merchant prince"),
    "a portfolio of people backed": dict(tribal="the camps and hunters given seed and stock, who give back in turn",
                                         magic="the ventures, artists and scholars a patron has backed",
                                         note="same"),
    "a following that turns out": dict(tribal="the young of every clan, who come when called",
                                       magic="the commons of the cities, who turn out when called",
                                       note="same; the route reads as a firebrand of the commons"),
    "a unit that trusts its leader": dict(tribal="a war band that trusts its leader", magic="a company that trusts "
                                                                                         "its captain",
                                          note="same; the route reads as a war-leader"),
    "a signature work and its audience": dict(tribal="a song or a feat every fire knows, and those who come to hear",
                                              magic="a signature work of the realm, and its audience", note="same"),
    "a living tradition kept": dict(tribal="the songs, crafts and rites of the clans, kept alive",
                                    magic="the realm's old crafts and rites, kept alive", note="same"),
    "a web of groups that help each other": dict(tribal="camps that share the winter stores",
                                                 magic="towns and guilds that help each other", note="same"),
    "a stretch of land kept alive": dict(tribal="a valley kept for the herds and the young trees",
                                         magic="a wild of the realm kept under ward", note="same"),
}
