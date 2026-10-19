# Chroma content packs, shared core: a work that outlives you (the Historic height's marker for the public callings).
# Pathways and packs thread, 2026-10-19, for aims version 1 (chroma-ideas/next-table-2026-10-19/plan.md, section 5;
# Emren 10-19 11:38 UTC: "1. Recommended", the three heights). Fields as in chroma-library/earth_perks_titles.py.
#
# SWITCHED OFF. batch.py reads TITLES, PERKS and ROLES from every core/*.py; this file holds none of them, so it changes
# no life. The Engine reads PERKS_AIMS and ROLES_AIMS only with its aims switch on, and joins each loaded pack's
# LEGACY_<PACK> (chroma-packs/<pack>/aims.py) into the one rule below, as it joins EXTEND_<PACK> into a base rule.
#
# The heights (plan.md section 5): Known (a leader in a place or a field), Notable (known across the country, or a
# summit), Historic (head of a state, an order or a movement, or a work or discovery that outlives them). Head of a
# state, an order or a movement already exist as titles ([head of government], [founder of a movement]); a work that
# outlives the person did not. This perk is that work, whatever it is: a book still read, a part still quoted, a
# finding still taught, a reform still in force, a record still kept, a piece in the national collection. It comes
# after long years at the top of a calling's ladder, and late; every pack says who can earn it (LEGACY_<PACK>).
#
# All five colors as ways, as the reach ladder's top rungs (core/reach.py): what outlives a person can be a law kept,
# a theory, a fortune's foundation, a song or a forest planted. It never fades (skill_half None).
#
# In other worlds (the realm-ready rule, plan.md section 2): the same height in every realm. Tribal: a telling, a
# carving, a way of hunting or a peace that the bands keep after the person is gone. Magic: a work the chroniclers
# record, a spell or a law the Orders keep, a hall or a house that still stands.

PERKS_AIMS = [
  dict(name="a work that outlives you", kind="standing", ways="W U B R G", odds=.02, skill_half=None, retires=None,
       ages=(35, 110), share=.003,   # estimate: people whose work is still used, read, seen or quoted by name a generation
                                     # after them (national figures, the authors and artists in the histories, the
                                     # scientists in the textbooks, local builders of what lasts); higher than real,
                                     # as Emren asked for the summits (10-06 14:41, "not super unrealistically")
       say="made something that will outlive them",
       gained="long years at the top of a calling: a book still in print, a part people still quote, a finding in the "
              "textbooks, a reform still in force, a record others keep using, a work in the national collection",
       lost="never; it stays in the story after death",
       needs="[known across the country], a summit or a standing perk at the top of a pack's road, held for years "
             "(each pack's LEGACY_<PACK> in its aims.py)"),
]

# Its form in the game's other worlds, as the packs' worlds.py.
WORLDS_AIMS = {
    "a work that outlives you": dict(tribal="a telling, a carving or a way the bands keep after you are gone",
                                     magic="a work the chroniclers will record", note="same"),
}

# The rule, in earth_rules.ROLES syntax. The Engine sets req to the or of the loaded packs' LEGACY_<PACK>; nothing
# else gives it. The rate is per year while the req holds (rules are checked every four weeks).
ROLES_AIMS = {
    "a work that outlives you": dict(req="LEGACY", rate=0.03, weight="colors"),
}
