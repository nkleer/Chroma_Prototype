# Chroma content pack: Art and Writing. The pack in the other worlds.
# Pathways and packs thread, 2026-10-10, in the shape of ../stage/worlds.py, after Emren (10-05 21:37): modern world
# conditions and terms first, "but dont forget that applications must be feasible for other wordly setting, even
# including supernatural sometimes." The catalogue stays in modern Earth terms; this file gives each title and perk its
# form in the game's tribal and magic worlds (chroma-game/prototype/story.py, SETTINGS and WORLD), so the pathway keeps
# the same shape everywhere: the same rungs, doors, steps and falls. Plain data for the Library and the game; nothing
# runs.
#
# The shape of art and writing in each world:
#   earth   school art rooms, evening life classes, poetry nights, art schools, walls and commissions, studios,
#           galleries, publishers, prizes, the national collection.
#   tribal  the band paints the rock at its painting place and the great cave at the winter camp, marks its drums,
#           bowls, shields and hides, and carves masks, figures and bone; verses are spoken at the fire and the best are
#           repeated by every band at the gatherings. Carvings travel by trade. No writing: the writer's road is the
#           maker of verses and long tellings.
#   magic   walled cities with an academy of arts, a painters' and a craft guild with marks and ranks, illuminators for
#           the books of the Orders and the printers, picture dealers with halls on the square, court painters and the
#           chronicler of the realm; poets read in the taverns and the academy gives laurels.
#
# Supernatural ways are possible sometimes and never forced: world-only moments (art-worlds.lib), each optional, each
# with a price, and never resting on the person's own gift (round 5's rule): an enchanter's varnish, a hedge-witch's
# pigment. Modern Earth has no magic.
#
# Fields: tribal and magic, the form in that world; note, how it maps: "same rung" when the role exists as it is,
# "nearest" when a stand-in keeps the pathway's shape.

WORLDS_ART = {
    # ------------------------------------------------ community and status
    "open-mic poet": dict(tribal="a speaker of verses at the band's fire on the long nights",
                          magic="a reader at the poets' night in the tavern", note="same rung"),
    "life-drawing regular": dict(tribal="one who draws on the rock with the others at the painting place",
                                 magic="a sketcher at the academy's evening hall", note="same rung"),
    "art school student": dict(tribal="apprentice to the painter of the great cave, for three winters",
                               magic="a student at the academy of arts", note="tribal: nearest; magic: same rung"),
    # ------------------------------------------------ careers
    "street artist": dict(tribal="painter of the shelter walls, the hides and the shields",
                          magic="painter of the city's walls and shop signs", note="same rung"),
    "illustrator for hire": dict(tribal="marker of drums, bowls and shields for anyone who asks",
                                 magic="an illuminator for hire: books, maps and broadsheets", note="same rung"),
    "painter or sculptor": dict(tribal="the cave painter or the carver of the band",
                                magic="a painter or sculptor of the guild", note="same rung"),
    "art teacher": dict(tribal="the one who teaches the children the marks and the patterns",
                        magic="a drawing master", note="same rung"),
    "gallery owner": dict(tribal="the trader in carvings at the great gatherings",
                          magic="a picture dealer with a hall on the square",
                          note="tribal: nearest (no shop: the trade at the gathering); magic: same rung"),
    "master craftsperson": dict(tribal="the master carver whose work is traded far",
                                magic="a master of the craft guild", note="same rung"),
    # ------------------------------------------------ summits
    "renowned artist": dict(tribal="the painter whose cave every band visits", magic="court painter",
                            note="same rung"),
    "celebrated author": dict(tribal="the maker of the verses every band repeats",
                              magic="chronicler of the realm, whose books are copied",
                              note="tribal: nearest (no writing); magic: same rung"),
    # ------------------------------------------------ base titles the pathway uses
    "novelist": dict(tribal="a maker of long tellings", magic="a writer of books", note="tribal: nearest"),
    "craft maker": dict(tribal="a carver, potter or weaver", magic="a journeyman of the craft guild",
                        note="same rung"),
    # ------------------------------------------------ perks
    "writing poems": dict(tribal="making verses", magic="writing verse", note="same"),
    "illustration": dict(tribal="painted patterns", magic="illumination", note="same"),
    "sculpting": dict(tribal="carving", magic="sculpture", note="same"),
    "art school degree": dict(tribal="the painter's leave to paint alone", magic="the academy's seal",
                              note="tribal: nearest"),
    "a publishing contract": dict(tribal="a place for one's tellings at the gathering", magic="a printer's contract",
                                  note="tribal: nearest"),
    "a maker's hallmark": dict(tribal="the band's sign cut beside one's own", magic="the guild's mark", note="same"),
    "a name in the art world": dict(tribal="a name among the traders", magic="a name at court and in the salons",
                                    note="same"),
    "a prize for writing": dict(tribal="the elders' honour at the gathering", magic="a laurel from the academy",
                                note="same"),
    "a mural the town loves": dict(tribal="a shelter wall the band loves", magic="a wall the quarter loves",
                                   note="same"),
    "pupils who remember you": dict(tribal="children who keep your patterns", magic="pupils who remember you",
                                    note="same"),
    "a dealer who sells your work": dict(tribal="a trader who carries your carvings", magic="a dealer",
                                         note="same"),
    "a circle of artists": dict(tribal="the ones who paint beside you", magic="a circle of the studio", note="same"),
    "a body of work": dict(tribal="carvings stored in the cave", magic="a body of work", note="same"),
    "works in collectors' hands": dict(tribal="pieces in other bands' hands", magic="pieces in noble houses",
                                       note="same"),
    "royalties": dict(tribal="a share of every trade in one's patterns", magic="royalties from the printers",
                      note="tribal: nearest"),
}

# World-only moments (art-worlds.lib), each optional and each with a price.
WORLD_ONLY_ART = {
    "the painted cave at the winter camp": dict(only="tribal", kind="crossing",
                                                what="the band's great cave wall for the midwinter gathering: the "
                                                     "elders choose who paints it, and what"),
    "the carver's mask for the dead": dict(only="tribal", kind="crossing",
                                           what="a mask for the dead chief's mourning, carved in the old way"),
    "the queen's portrait sitting": dict(only="magic", kind="crossing",
                                         what="the court wants a portrait; an enchanter's varnish can make it smile, "
                                              "with the Order's leave"),
    "the illuminated book for the cathedral": dict(only="magic", kind="door",
                                                   what="a year's work on a great book for an Order's cathedral"),
}
