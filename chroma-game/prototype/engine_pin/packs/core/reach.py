# Chroma content packs, shared core: the reach ladder (how far a person's name carries).
# Pathways and packs thread, 2026-10-05. Every pathway pack (Science, Politics, Art and Writing, Military...) uses the
# same ladder, so fame is earned inside a pathway and never becomes a separate meter (Emren's Science document: "visibility
# must not become a hidden universal victory score"). Fields as in chroma-library/earth_perks_titles.py.
#
# The ladder:
#   known in town            the base perk [good name in town] (and [local hero], [name on the local scene])
#   known in the field       the base perk [name in the field]
#   known across the country new: national news, a national office, a bestseller, a famous case
#   a household name         new: most adults in the country know the name
#
# Both new rungs are standing perks with all five colors as ways: being known helps any way of acting a little, the
# rules-keeper's appeal and the rebel's alike. Higher rungs of a pathway need some reach (a minister needs [known across
# the country] in most cases), and reach can also come without a title: a video that spreads, a rescue in the papers,
# a scandal. It fades when the person drops from view (skill_half: years for the name to fade by half).

PERKS = [
  dict(name="known across the country", kind="standing", ways="W U B R G", odds=.03, skill_half=8, retires=None,
       ages=(10, 110), share=.003,   # estimate: people a national audience would recognise by name or face at some
                                     # point in life (national politicians, broadcasters, athletes, authors,
                                     # people in famous cases)
       say="known across the country",
       gained="a national office, a bestseller, a national team, a famous case, a television series; a video or a "
              "scandal that reaches every paper; [name in the field] carried into the national news",
       lost="years out of the news",
       needs="[good name in town], [name in the field], [following online] or a title at the top of a pathway; or "
             "one moment the whole country sees"),
  dict(name="a household name", kind="standing", ways="W U B R G", odds=.04, skill_half=15, retires=None,
       ages=(12, 110), share=.0003,   # estimate: a few thousand living people in a large country
       say="a household name",
       gained="years at the top of a pathway with [known across the country]; one event everyone remembers",
       lost="decades out of view; the name lives on in the story after death",
       needs="[known across the country]"),
]
