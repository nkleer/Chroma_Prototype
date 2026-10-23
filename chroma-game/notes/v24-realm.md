# v24 game mechanics in a magic realm

How each v24 game mechanic reads when the world is not Modern Earth (Release's R1, for the realm-ready rule in
`CONTRIBUTING.md`). Each one is built on the engine's world-agnostic parts (colours, needs, means, people, titles,
spheres) and takes its words from the Library or a pack, so a realm brings its own words, not new code.

**Hover arrows.** The arrows show which way a choice moves needs, means, people and titles, with three sizes and size
words, never numbers. Nothing in them names an Earth thing: a realm's needs and titles come from its own data, so in a
magic realm an arrow can point at a rank in an order or at standing with a temple as easily as at a job title.

**Footprints.** A footprint is one of six kinds (people, places, means, marks, doors, lessons), and the game only
counts and tells them; their words come from the Library's `footprint_names.py`. Today that file has one word set,
written for Earth ("a club room or hall", "a sports club"), keyed by the engine's own haunt, role and mark keys. A magic
realm adds its own set on the same keys: a place becomes a tower or a shrine someone tends, a mark counts toward a rank
in an order, a door is an apprenticeship that opens, a lesson is a working learned. That is Library work; the game needs
no change for it.

**Aims and heights.** The ladders a life climbs are Library and pack data (the callings pack), and the heights rest on
standing in a sphere, not on any Earth institution. A realm brings its own ladders, such as the ranks of a magical
order, a druid's circle or a kingdom's court, and the game shows them the same way it shows a scientist's or a
politician's.

**Asks, steering and talk.** Asks, the steer between two ways and the talk replies are built on colours, needs, aims
and people, with no Earth content. The talk replies are short, plain game words; a realm that wants its own voice can
replace them with a Library line set without touching the logic.

**World answers display.** The "Your world" panel and the told lines read the Library's lines for the world being
played (`earth_world_lines.py` keys them earth, tribal and magic, and the magic set already speaks of decrees and
towers). The five rings (people, groups, places, the town's spheres, the realm) take the world's own names, so a magic
realm shows "The realm" where Earth shows "The country". The few game words around them (what the life kept doing, the
fair line) are plain English with no setting in them.
